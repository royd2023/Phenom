"""User authentication endpoints for U-CHS backend application."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional
import logging
import uuid
import hashlib
import jwt

from ..models.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
)
from ..core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


# In-memory user storage (replace with database in production)
users_storage: dict[str, dict] = {}
user_tokens: dict[str, str] = {}  # token -> user_id mapping


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(
        (password + settings.SECRET_KEY).encode()
    ).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        bool: True if password matches
    """
    return hash_password(plain_password) == hashed_password


def create_access_token(user_id: str, email: str) -> tuple[str, int]:
    """
    Create a JWT access token.

    Args:
        user_id: User ID
        email: User email

    Returns:
        tuple: (token, expires_in_seconds)
    """
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta

    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token, int(expires_delta.total_seconds())


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token

    Returns:
        dict: Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.JWTError as e:
        logger.warning(f"Invalid token: {str(e)}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserResponse:
    """
    Get current authenticated user from token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        UserResponse: Current user

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id or user_id not in users_storage:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_data = users_storage[user_id]
    return UserResponse(**user_data)


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate) -> Token:
    """
    Register a new user.

    Args:
        user_data: User registration data

    Returns:
        Token: Access token and user information
    """
    try:
        # Check if user already exists
        for user in users_storage.values():
            if user["email"] == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(user_data.password)

        user = {
            "id": user_id,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "role": user_data.role,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "is_active": True,
        }

        users_storage[user_id] = user

        # Create access token
        access_token, expires_in = create_access_token(user_id, user_data.email)
        user_tokens[access_token] = user_id

        # Create user response
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            created_at=user["created_at"],
            is_active=user["is_active"],
        )

        logger.info(f"New user registered: {user_data.email} (ID: {user_id})")

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
            user=user_response,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to register user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_user(credentials: UserLogin) -> Token:
    """
    Authenticate user and return access token.

    Args:
        credentials: User login credentials

    Returns:
        Token: Access token and user information
    """
    try:
        # Find user by email
        user = None
        user_id = None
        for uid, u in users_storage.items():
            if u["email"] == credentials.email:
                user = u
                user_id = uid
                break

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # Create access token
        access_token, expires_in = create_access_token(user_id, user["email"])
        user_tokens[access_token] = user_id

        # Create user response
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            created_at=user["created_at"],
            is_active=user["is_active"],
        )

        logger.info(f"User logged in: {credentials.email}")

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
            user=user_response,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to login user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to login: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        UserResponse: Current user information
    """
    return current_user


@router.post("/logout")
async def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Logout user by invalidating token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        dict: Logout confirmation
    """
    token = credentials.credentials

    # Remove token from storage
    if token in user_tokens:
        del user_tokens[token]

    logger.info("User logged out")

    return {"message": "Successfully logged out"}
