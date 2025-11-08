"""Storage service for managing images and files."""

import logging
from typing import Optional
import io
import uuid
from datetime import datetime, timedelta

from ..core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Service for managing file storage (Supabase/S3)."""

    def __init__(self):
        """Initialize storage service."""
        self.storage_type = self._determine_storage_type()
        self.supabase_client = None
        self.s3_client = None

        logger.info(f"Initializing Storage Service with type: {self.storage_type}")

        if self.storage_type == "supabase":
            self._init_supabase()
        elif self.storage_type == "s3":
            self._init_s3()
        else:
            logger.warning("Running in demo mode without cloud storage")

    def _determine_storage_type(self) -> str:
        """Determine which storage backend to use."""
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            return "supabase"
        elif settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            return "s3"
        else:
            return "local"

    def _init_supabase(self) -> None:
        """Initialize Supabase client."""
        try:
            from supabase import create_client, Client

            self.supabase_client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            self.storage_type = "local"

    def _init_s3(self) -> None:
        """Initialize S3 client."""
        try:
            import boto3

            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            logger.info("S3 client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize S3: {e}")
            self.storage_type = "local"

    async def upload_image(
        self,
        image_data: bytes,
        image_id: str,
        filename: str,
    ) -> str:
        """
        Upload image to storage.

        Args:
            image_data: Raw image bytes
            image_id: Unique image ID
            filename: Original filename

        Returns:
            str: URL to uploaded image
        """
        try:
            # Generate storage path
            timestamp = datetime.utcnow().strftime("%Y%m%d")
            file_extension = filename.split(".")[-1] if "." in filename else "jpg"
            storage_path = f"images/{timestamp}/{image_id}.{file_extension}"

            if self.storage_type == "supabase":
                return await self._upload_to_supabase(image_data, storage_path)
            elif self.storage_type == "s3":
                return await self._upload_to_s3(image_data, storage_path)
            else:
                return await self._upload_local(image_data, storage_path)

        except Exception as e:
            logger.error(f"Error uploading image: {e}", exc_info=True)
            raise

    async def _upload_to_supabase(self, data: bytes, path: str) -> str:
        """Upload to Supabase storage."""
        try:
            # Upload file
            result = self.supabase_client.storage.from_(settings.SUPABASE_BUCKET).upload(
                path=path,
                file=data,
                file_options={"content-type": "image/jpeg"}
            )

            # Get public URL
            url = self.supabase_client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path)

            logger.info(f"Uploaded to Supabase: {path}")
            return url

        except Exception as e:
            logger.error(f"Supabase upload failed: {e}")
            raise

    async def _upload_to_s3(self, data: bytes, path: str) -> str:
        """Upload to AWS S3."""
        try:
            # Upload file
            self.s3_client.put_object(
                Bucket=settings.S3_BUCKET,
                Key=path,
                Body=data,
                ContentType="image/jpeg"
            )

            # Generate URL
            url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{path}"

            logger.info(f"Uploaded to S3: {path}")
            return url

        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
            raise

    async def _upload_local(self, data: bytes, path: str) -> str:
        """Upload to local storage (demo mode)."""
        # In demo mode, return a mock URL
        url = f"http://localhost:8000/storage/{path}"
        logger.info(f"Demo mode: Mock upload to {path}")
        return url

    async def download_image(self, image_url: str) -> bytes:
        """
        Download image from storage.

        Args:
            image_url: URL to image

        Returns:
            bytes: Image data
        """
        try:
            if self.storage_type == "supabase":
                return await self._download_from_supabase(image_url)
            elif self.storage_type == "s3":
                return await self._download_from_s3(image_url)
            else:
                return await self._download_local(image_url)

        except Exception as e:
            logger.error(f"Error downloading image: {e}", exc_info=True)
            raise

    async def _download_from_supabase(self, url: str) -> bytes:
        """Download from Supabase storage."""
        try:
            # Extract path from URL
            path = url.split(f"{settings.SUPABASE_BUCKET}/")[-1]

            # Download file
            data = self.supabase_client.storage.from_(settings.SUPABASE_BUCKET).download(path)

            return data

        except Exception as e:
            logger.error(f"Supabase download failed: {e}")
            raise

    async def _download_from_s3(self, url: str) -> bytes:
        """Download from AWS S3."""
        try:
            # Extract path from URL
            path = url.split(f"{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/")[-1]

            # Download file
            response = self.s3_client.get_object(Bucket=settings.S3_BUCKET, Key=path)
            data = response['Body'].read()

            return data

        except Exception as e:
            logger.error(f"S3 download failed: {e}")
            raise

    async def _download_local(self, url: str) -> bytes:
        """Download from local storage (demo mode)."""
        # In demo mode, return mock image data
        logger.info(f"Demo mode: Mock download from {url}")
        # Return a small 1x1 PNG
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

    async def create_thumbnail(
        self,
        image_data: bytes,
        image_id: str,
        size: tuple = (256, 256),
    ) -> Optional[str]:
        """
        Create and upload thumbnail.

        Args:
            image_data: Original image bytes
            image_id: Image ID
            size: Thumbnail size (width, height)

        Returns:
            Optional[str]: URL to thumbnail, or None if failed
        """
        try:
            from PIL import Image

            # Create thumbnail
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(size, Image.Resampling.LANCZOS)

            # Convert to bytes
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=85)
            thumbnail_data = buffer.getvalue()

            # Upload thumbnail
            timestamp = datetime.utcnow().strftime("%Y%m%d")
            thumbnail_path = f"thumbnails/{timestamp}/{image_id}_thumb.jpg"

            if self.storage_type == "supabase":
                return await self._upload_to_supabase(thumbnail_data, thumbnail_path)
            elif self.storage_type == "s3":
                return await self._upload_to_s3(thumbnail_data, thumbnail_path)
            else:
                return await self._upload_local(thumbnail_data, thumbnail_path)

        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            return None

    async def upload_mask(
        self,
        mask_data: bytes,
        image_id: str,
        detection_id: str,
    ) -> str:
        """
        Upload segmentation mask.

        Args:
            mask_data: Mask image bytes
            image_id: Associated image ID
            detection_id: Detection ID

        Returns:
            str: URL to mask
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        mask_path = f"masks/{timestamp}/{image_id}/{detection_id}.png"

        if self.storage_type == "supabase":
            return await self._upload_to_supabase(mask_data, mask_path)
        elif self.storage_type == "s3":
            return await self._upload_to_s3(mask_data, mask_path)
        else:
            return await self._upload_local(mask_data, mask_path)

    async def upload_visualization(
        self,
        visualization_data: bytes,
        image_id: str,
        analysis_id: str,
    ) -> str:
        """
        Upload analysis visualization.

        Args:
            visualization_data: Visualization image bytes
            image_id: Associated image ID
            analysis_id: Analysis ID

        Returns:
            str: URL to visualization
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        vis_path = f"visualizations/{timestamp}/{image_id}/{analysis_id}.png"

        if self.storage_type == "supabase":
            return await self._upload_to_supabase(visualization_data, vis_path)
        elif self.storage_type == "s3":
            return await self._upload_to_s3(visualization_data, vis_path)
        else:
            return await self._upload_local(visualization_data, vis_path)

    async def get_image_url(self, image_id: str) -> Optional[str]:
        """
        Get URL for an image by ID.

        Args:
            image_id: Image ID

        Returns:
            Optional[str]: Image URL, or None if not found
        """
        # This is a simplified implementation
        # In production, you'd query a database for the actual URL
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        path = f"images/{timestamp}/{image_id}.jpg"

        if self.storage_type == "local":
            return f"http://localhost:8000/storage/{path}"

        # For cloud storage, construct URL based on storage type
        return None

    async def delete_image(self, image_id: str) -> None:
        """
        Delete an image from storage.

        Args:
            image_id: Image ID to delete
        """
        logger.info(f"Deleting image {image_id}")
        # TODO: Implement actual deletion based on storage type


# Global storage service instance
_storage_service: Optional[StorageService] = None


def get_storage_service() -> StorageService:
    """
    Get or create storage service instance.

    Returns:
        StorageService: Singleton storage service instance
    """
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service
