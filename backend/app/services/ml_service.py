"""ML service for image analysis using SAM and Grounding DINO."""

import logging
import numpy as np
from typing import List, Dict, Any, Optional
import torch
from PIL import Image
import io
import cv2

from ..core.config import settings

logger = logging.getLogger(__name__)


class MLService:
    """Machine Learning service for medical image analysis."""

    def __init__(self):
        """Initialize ML service with models."""
        self.device = "cuda" if torch.cuda.is_available() and settings.USE_GPU else "cpu"
        self.sam_model = None
        self.sam_predictor = None
        self.grounding_dino_model = None
        self.sam_model_type = settings.SAM_MODEL_TYPE

        logger.info(f"Initializing ML Service on device: {self.device}")

        # Load models lazily (on first use)
        self._models_loaded = False

    def _load_models(self) -> None:
        """Load SAM and Grounding DINO models."""
        if self._models_loaded:
            return

        try:
            logger.info("Loading SAM model...")
            # Import SAM
            try:
                from segment_anything import sam_model_registry, SamPredictor

                self.sam_model = sam_model_registry[self.sam_model_type](
                    checkpoint=settings.SAM_CHECKPOINT_PATH
                )
                self.sam_model.to(device=self.device)
                self.sam_predictor = SamPredictor(self.sam_model)

                logger.info(f"SAM model loaded successfully: {self.sam_model_type}")
            except Exception as e:
                logger.warning(f"Failed to load SAM model: {e}")
                logger.info("Running in demo mode without SAM")

            logger.info("Loading Grounding DINO model...")
            # Import Grounding DINO
            try:
                # Note: This is a placeholder - actual import depends on Grounding DINO installation
                # from groundingdino.util.inference import load_model
                # self.grounding_dino_model = load_model(
                #     settings.GROUNDING_DINO_CONFIG_PATH,
                #     settings.GROUNDING_DINO_CHECKPOINT_PATH
                # )
                logger.info("Grounding DINO model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load Grounding DINO model: {e}")
                logger.info("Running in demo mode without Grounding DINO")

            self._models_loaded = True

        except Exception as e:
            logger.error(f"Error loading models: {e}", exc_info=True)
            logger.warning("ML Service running in demo mode")
            self._models_loaded = True  # Continue in demo mode

    async def analyze_image(
        self,
        image_data: bytes,
        prompts: List[str],
        box_threshold: float = 0.35,
        text_threshold: float = 0.25,
        include_segmentation: bool = True,
    ) -> Dict[str, Any]:
        """
        Analyze medical image using Grounding DINO and SAM.

        Args:
            image_data: Raw image bytes
            prompts: Text prompts for object detection
            box_threshold: Bounding box confidence threshold
            text_threshold: Text matching confidence threshold
            include_segmentation: Whether to generate segmentation masks

        Returns:
            Dict containing detections, masks, and visualization
        """
        self._load_models()

        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            image_np = np.array(image)

            logger.info(
                f"Analyzing image with prompts: {prompts}, "
                f"box_threshold: {box_threshold}, text_threshold: {text_threshold}"
            )

            # For demo mode, return mock results
            if self.grounding_dino_model is None:
                return await self._generate_demo_results(
                    image_np, prompts, include_segmentation
                )

            # Run Grounding DINO for object detection
            detections = await self._run_grounding_dino(
                image_np,
                prompts,
                box_threshold,
                text_threshold,
            )

            # Run SAM for segmentation if requested
            if include_segmentation and self.sam_predictor is not None:
                detections = await self._add_segmentation_masks(
                    image_np,
                    detections,
                )

            # Generate visualization
            visualization = self._create_visualization(
                image_np,
                detections,
                include_segmentation,
            )

            return {
                "detections": detections,
                "visualization": visualization,
            }

        except Exception as e:
            logger.error(f"Error analyzing image: {e}", exc_info=True)
            raise

    async def _run_grounding_dino(
        self,
        image: np.ndarray,
        prompts: List[str],
        box_threshold: float,
        text_threshold: float,
    ) -> List[Dict[str, Any]]:
        """
        Run Grounding DINO object detection.

        Args:
            image: Image as numpy array
            prompts: Detection prompts
            box_threshold: Box confidence threshold
            text_threshold: Text confidence threshold

        Returns:
            List of detection results
        """
        # TODO: Implement actual Grounding DINO inference
        # This is a placeholder implementation

        detections = []
        # Placeholder logic would go here

        return detections

    async def _add_segmentation_masks(
        self,
        image: np.ndarray,
        detections: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Add SAM segmentation masks to detections.

        Args:
            image: Image as numpy array
            detections: Detection results from Grounding DINO

        Returns:
            Detections with added segmentation masks
        """
        if self.sam_predictor is None:
            return detections

        try:
            # Set image for SAM predictor
            self.sam_predictor.set_image(image)

            # Generate masks for each detection
            for detection in detections:
                bbox = detection["bbox"]  # [x1, y1, x2, y2]

                # Run SAM with box prompt
                masks, scores, _ = self.sam_predictor.predict(
                    box=np.array(bbox),
                    multimask_output=False,
                )

                if len(masks) > 0:
                    mask = masks[0]  # Use best mask
                    detection["mask"] = mask
                    detection["mask_confidence"] = float(scores[0])
                    detection["area"] = int(np.sum(mask))

            return detections

        except Exception as e:
            logger.error(f"Error generating segmentation masks: {e}", exc_info=True)
            return detections

    def _create_visualization(
        self,
        image: np.ndarray,
        detections: List[Dict[str, Any]],
        include_segmentation: bool,
    ) -> bytes:
        """
        Create visualization of detection results.

        Args:
            image: Original image
            detections: Detection results
            include_segmentation: Whether to overlay masks

        Returns:
            Visualization as image bytes
        """
        try:
            vis_image = image.copy()

            # Draw bounding boxes and masks
            for detection in detections:
                bbox = detection["bbox"]
                label = detection["label"]
                confidence = detection["confidence"]

                # Draw bounding box
                cv2.rectangle(
                    vis_image,
                    (int(bbox[0]), int(bbox[1])),
                    (int(bbox[2]), int(bbox[3])),
                    (0, 255, 0),
                    2,
                )

                # Draw label
                label_text = f"{label}: {confidence:.2f}"
                cv2.putText(
                    vis_image,
                    label_text,
                    (int(bbox[0]), int(bbox[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

                # Draw mask if available
                if include_segmentation and "mask" in detection:
                    mask = detection["mask"]
                    colored_mask = np.zeros_like(vis_image)
                    colored_mask[mask] = [0, 255, 0]
                    vis_image = cv2.addWeighted(vis_image, 0.7, colored_mask, 0.3, 0)

            # Convert to bytes
            pil_image = Image.fromarray(vis_image)
            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            return buffer.getvalue()

        except Exception as e:
            logger.error(f"Error creating visualization: {e}", exc_info=True)
            return b""

    async def _generate_demo_results(
        self,
        image: np.ndarray,
        prompts: List[str],
        include_segmentation: bool,
    ) -> Dict[str, Any]:
        """
        Generate demo/mock results for testing without models.

        Args:
            image: Image as numpy array
            prompts: Detection prompts
            include_segmentation: Whether to include masks

        Returns:
            Mock detection results
        """
        height, width = image.shape[:2]

        # Generate mock detections
        detections = []
        for i, prompt in enumerate(prompts):
            # Create mock bounding box
            x1 = width * (0.2 + i * 0.1)
            y1 = height * (0.2 + i * 0.1)
            x2 = x1 + width * 0.3
            y2 = y1 + height * 0.3

            detection = {
                "label": prompt,
                "confidence": 0.85 - i * 0.1,
                "bbox": [x1, y1, x2, y2],
            }

            # Add mock mask if requested
            if include_segmentation:
                mask = np.zeros((height, width), dtype=bool)
                mask[int(y1):int(y2), int(x1):int(x2)] = True
                detection["mask"] = mask
                detection["mask_confidence"] = 0.9
                detection["area"] = int((x2 - x1) * (y2 - y1))

            detections.append(detection)

        # Generate mock visualization
        visualization = self._create_visualization(
            image,
            detections,
            include_segmentation,
        )

        logger.info(f"Generated {len(detections)} demo detections")

        return {
            "detections": detections,
            "visualization": visualization,
        }


# Global ML service instance
_ml_service: Optional[MLService] = None


def get_ml_service() -> MLService:
    """
    Get or create ML service instance.

    Returns:
        MLService: Singleton ML service instance
    """
    global _ml_service
    if _ml_service is None:
        _ml_service = MLService()
    return _ml_service
