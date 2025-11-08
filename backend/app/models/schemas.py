"""Pydantic schemas for U-CHS backend application."""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AnalysisStatus(str, Enum):
    """Analysis status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageType(str, Enum):
    """Image type enumeration."""
    ULTRASOUND = "ultrasound"
    CT_SCAN = "ct_scan"
    MRI = "mri"
    XRAY = "xray"
    OTHER = "other"


# Health Check Schemas
class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    environment: str
    services: Dict[str, bool] = Field(default_factory=dict)


# User Schemas
class UserCreate(BaseModel):
    """User creation schema."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(default="user")

    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Image Schemas
class ImageMetadata(BaseModel):
    """Image metadata schema."""
    width: int
    height: int
    format: str
    size_bytes: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    image_type: Optional[ImageType] = None
    patient_id: Optional[str] = None
    study_id: Optional[str] = None
    modality: Optional[str] = None


class ImageUploadRequest(BaseModel):
    """Image upload request schema."""
    image_data: str = Field(..., description="Base64 encoded image data")
    filename: str = Field(..., min_length=1)
    image_type: Optional[ImageType] = ImageType.ULTRASOUND
    patient_id: Optional[str] = None
    study_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ImageUploadResponse(BaseModel):
    """Image upload response schema."""
    image_id: str
    image_url: str
    thumbnail_url: Optional[str] = None
    metadata: ImageMetadata
    message: str = "Image uploaded successfully"


# Analysis Schemas
class BoundingBox(BaseModel):
    """Bounding box schema."""
    x: float = Field(..., ge=0, description="X coordinate of top-left corner")
    y: float = Field(..., ge=0, description="Y coordinate of top-left corner")
    width: float = Field(..., gt=0, description="Width of bounding box")
    height: float = Field(..., gt=0, description="Height of bounding box")

    @property
    def x2(self) -> float:
        """Get x coordinate of bottom-right corner."""
        return self.x + self.width

    @property
    def y2(self) -> float:
        """Get y coordinate of bottom-right corner."""
        return self.y + self.height

    def to_xyxy(self) -> List[float]:
        """Convert to [x1, y1, x2, y2] format."""
        return [self.x, self.y, self.x2, self.y2]


class SegmentationMask(BaseModel):
    """Segmentation mask schema."""
    mask_url: str = Field(..., description="URL to segmentation mask image")
    mask_data: Optional[List[List[int]]] = Field(None, description="Binary mask data")
    area_pixels: int = Field(..., ge=0, description="Area in pixels")
    area_mm2: Optional[float] = Field(None, ge=0, description="Area in mm²")
    perimeter_pixels: Optional[float] = Field(None, ge=0)
    confidence: float = Field(..., ge=0, le=1, description="Segmentation confidence")


class DetectionResult(BaseModel):
    """Detection result schema."""
    label: str = Field(..., description="Detected object label")
    confidence: float = Field(..., ge=0, le=1, description="Detection confidence")
    bounding_box: BoundingBox
    segmentation: Optional[SegmentationMask] = None
    attributes: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AnalysisRequest(BaseModel):
    """Analysis request schema."""
    image_id: str = Field(..., description="ID of uploaded image")
    prompts: List[str] = Field(..., min_items=1, description="Text prompts for detection")
    box_threshold: float = Field(default=0.35, ge=0, le=1)
    text_threshold: float = Field(default=0.25, ge=0, le=1)
    include_segmentation: bool = Field(default=True)
    include_visualization: bool = Field(default=True)

    @validator("prompts")
    def validate_prompts(cls, v):
        """Validate prompts list."""
        if not v:
            raise ValueError("At least one prompt is required")
        if any(not prompt.strip() for prompt in v):
            raise ValueError("Prompts cannot be empty strings")
        return [prompt.strip() for prompt in v]


class AnalysisResponse(BaseModel):
    """Analysis response schema."""
    analysis_id: str
    image_id: str
    status: AnalysisStatus
    detections: List[DetectionResult] = Field(default_factory=list)
    visualization_url: Optional[str] = None
    processing_time_ms: float
    model_info: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None


class AnalysisListResponse(BaseModel):
    """Analysis list response schema."""
    analyses: List[AnalysisResponse]
    total: int
    page: int = 1
    page_size: int = 10
    has_more: bool = False


# Error Schemas
class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
