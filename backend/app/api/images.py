"""Image management endpoints for U-CHS backend application."""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
import logging
import uuid
import base64
from datetime import datetime

from ..models.schemas import (
    ImageUploadRequest,
    ImageUploadResponse,
    ImageMetadata,
    ImageType,
)
from ..services.storage_service import StorageService, get_storage_service
from ..core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# In-memory storage for image metadata (replace with database in production)
image_metadata_storage: dict[str, ImageMetadata] = {}


def validate_image_data(image_data: bytes) -> None:
    """
    Validate image data.

    Args:
        image_data: Raw image bytes

    Raises:
        HTTPException: If image validation fails
    """
    # Check file size
    if len(image_data) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Image size exceeds maximum allowed size of {settings.MAX_IMAGE_SIZE} bytes"
        )

    # Check if it's a valid image (basic check)
    if not image_data.startswith(b'\xff\xd8\xff') and not image_data.startswith(b'\x89PNG'):
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Only JPEG and PNG are supported."
        )


@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    request: ImageUploadRequest,
    storage_service: StorageService = Depends(get_storage_service),
) -> ImageUploadResponse:
    """
    Upload a new image.

    Args:
        request: Image upload request with base64 encoded data
        storage_service: Storage service instance

    Returns:
        ImageUploadResponse: Upload response with image ID and URL
    """
    try:
        # Decode base64 image data
        try:
            # Remove data URL prefix if present
            if "," in request.image_data:
                request.image_data = request.image_data.split(",", 1)[1]

            image_bytes = base64.b64decode(request.image_data)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid base64 image data: {str(e)}"
            )

        # Validate image
        validate_image_data(image_bytes)

        # Generate unique image ID
        image_id = str(uuid.uuid4())

        # Determine image format
        if image_bytes.startswith(b'\xff\xd8\xff'):
            image_format = "jpeg"
        elif image_bytes.startswith(b'\x89PNG'):
            image_format = "png"
        else:
            image_format = "unknown"

        # Upload image to storage
        image_url = await storage_service.upload_image(
            image_data=image_bytes,
            image_id=image_id,
            filename=request.filename,
        )

        # Create thumbnail (optional)
        thumbnail_url = await storage_service.create_thumbnail(
            image_data=image_bytes,
            image_id=image_id,
        )

        # Get image dimensions (would require PIL/Pillow in production)
        # For now, use placeholder values
        width, height = 512, 512  # TODO: Get actual dimensions

        # Create metadata
        metadata = ImageMetadata(
            width=width,
            height=height,
            format=image_format,
            size_bytes=len(image_bytes),
            uploaded_at=datetime.utcnow(),
            image_type=request.image_type,
            patient_id=request.patient_id,
            study_id=request.study_id,
            modality=request.metadata.get("modality") if request.metadata else None,
        )

        # Store metadata
        image_metadata_storage[image_id] = metadata

        logger.info(
            f"Uploaded image {image_id} ({request.filename}) - "
            f"Size: {len(image_bytes)} bytes, Type: {request.image_type}"
        )

        return ImageUploadResponse(
            image_id=image_id,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
            metadata=metadata,
            message="Image uploaded successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.post("/upload-file", response_model=ImageUploadResponse)
async def upload_image_file(
    file: UploadFile = File(...),
    image_type: Optional[ImageType] = ImageType.ULTRASOUND,
    patient_id: Optional[str] = None,
    study_id: Optional[str] = None,
    storage_service: StorageService = Depends(get_storage_service),
) -> ImageUploadResponse:
    """
    Upload image file directly (multipart/form-data).

    Args:
        file: Uploaded file
        image_type: Type of crop image
        patient_id: Optional patient ID
        study_id: Optional study ID
        storage_service: Storage service instance

    Returns:
        ImageUploadResponse: Upload response with image ID and URL
    """
    try:
        # Read file content
        image_bytes = await file.read()

        # Validate image
        validate_image_data(image_bytes)

        # Convert to base64 and use regular upload endpoint logic
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        request = ImageUploadRequest(
            image_data=image_base64,
            filename=file.filename or "uploaded_image",
            image_type=image_type,
            patient_id=patient_id,
            study_id=study_id,
        )

        return await upload_image(request, storage_service)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload image file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload image file: {str(e)}"
        )


@router.get("/{image_id}", response_model=ImageMetadata)
async def get_image_metadata(image_id: str) -> ImageMetadata:
    """
    Get image metadata by ID.

    Args:
        image_id: Unique image ID

    Returns:
        ImageMetadata: Image metadata
    """
    if image_id not in image_metadata_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Image {image_id} not found"
        )

    return image_metadata_storage[image_id]


@router.get("/", response_model=List[ImageMetadata])
async def list_images(
    patient_id: Optional[str] = None,
    study_id: Optional[str] = None,
    image_type: Optional[ImageType] = None,
    limit: int = 100,
) -> List[ImageMetadata]:
    """
    List images with optional filtering.

    Args:
        patient_id: Filter by patient ID
        study_id: Filter by study ID
        image_type: Filter by image type
        limit: Maximum number of results

    Returns:
        List[ImageMetadata]: List of image metadata
    """
    images = list(image_metadata_storage.values())

    # Apply filters
    if patient_id:
        images = [img for img in images if img.patient_id == patient_id]
    if study_id:
        images = [img for img in images if img.study_id == study_id]
    if image_type:
        images = [img for img in images if img.image_type == image_type]

    # Sort by upload time, newest first
    images.sort(key=lambda x: x.uploaded_at, reverse=True)

    # Apply limit
    return images[:limit]


@router.delete("/{image_id}")
async def delete_image(
    image_id: str,
    storage_service: StorageService = Depends(get_storage_service),
) -> dict:
    """
    Delete an image and its metadata.

    Args:
        image_id: Unique image ID
        storage_service: Storage service instance

    Returns:
        dict: Deletion confirmation
    """
    if image_id not in image_metadata_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Image {image_id} not found"
        )

    try:
        # Delete from storage
        await storage_service.delete_image(image_id)

        # Delete metadata
        del image_metadata_storage[image_id]

        logger.info(f"Deleted image {image_id}")

        return {"message": f"Image {image_id} deleted successfully"}

    except Exception as e:
        logger.error(f"Failed to delete image {image_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete image: {str(e)}"
        )
