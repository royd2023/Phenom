"""Image analysis endpoints for U-CHS backend application."""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
import logging
import uuid
from datetime import datetime
import time

from ..models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisStatus,
    DetectionResult,
    BoundingBox,
    SegmentationMask,
)
from ..services.ml_service import MLService, get_ml_service
from ..services.storage_service import StorageService, get_storage_service

logger = logging.getLogger(__name__)
router = APIRouter()


# In-memory storage for analysis results (replace with database in production)
analysis_storage: dict[str, AnalysisResponse] = {}


async def run_analysis_task(
    analysis_id: str,
    image_id: str,
    image_url: str,
    prompts: List[str],
    box_threshold: float,
    text_threshold: float,
    include_segmentation: bool,
    ml_service: MLService,
    storage_service: StorageService,
) -> None:
    """
    Background task to run image analysis.

    Args:
        analysis_id: Unique analysis ID
        image_id: Image ID
        image_url: URL to image
        prompts: Detection prompts
        box_threshold: Bounding box threshold
        text_threshold: Text threshold
        include_segmentation: Whether to include segmentation
        ml_service: ML service instance
        storage_service: Storage service instance
    """
    try:
        logger.info(f"Starting analysis {analysis_id} for image {image_id}")

        # Update status to processing
        if analysis_id in analysis_storage:
            analysis_storage[analysis_id].status = AnalysisStatus.PROCESSING

        start_time = time.time()

        # Download image from storage
        image_data = await storage_service.download_image(image_url)

        # Run ML inference
        results = await ml_service.analyze_image(
            image_data=image_data,
            prompts=prompts,
            box_threshold=box_threshold,
            text_threshold=text_threshold,
            include_segmentation=include_segmentation,
        )

        processing_time = (time.time() - start_time) * 1000  # Convert to ms

        # Convert results to schema format
        detections: List[DetectionResult] = []
        for result in results.get("detections", []):
            bbox = BoundingBox(
                x=result["bbox"][0],
                y=result["bbox"][1],
                width=result["bbox"][2] - result["bbox"][0],
                height=result["bbox"][3] - result["bbox"][1],
            )

            segmentation = None
            if include_segmentation and "mask" in result:
                # Upload mask to storage
                mask_url = await storage_service.upload_mask(
                    mask_data=result["mask"],
                    image_id=image_id,
                    detection_id=str(uuid.uuid4()),
                )

                segmentation = SegmentationMask(
                    mask_url=mask_url,
                    area_pixels=int(result.get("area", 0)),
                    confidence=result.get("mask_confidence", result["confidence"]),
                )

            detection = DetectionResult(
                label=result["label"],
                confidence=result["confidence"],
                bounding_box=bbox,
                segmentation=segmentation,
                attributes=result.get("attributes", {}),
            )
            detections.append(detection)

        # Generate visualization if requested
        visualization_url = None
        if results.get("visualization"):
            visualization_url = await storage_service.upload_visualization(
                visualization_data=results["visualization"],
                image_id=image_id,
                analysis_id=analysis_id,
            )

        # Update analysis result
        analysis_storage[analysis_id] = AnalysisResponse(
            analysis_id=analysis_id,
            image_id=image_id,
            status=AnalysisStatus.COMPLETED,
            detections=detections,
            visualization_url=visualization_url,
            processing_time_ms=processing_time,
            model_info={
                "sam_model": ml_service.sam_model_type if hasattr(ml_service, 'sam_model_type') else "unknown",
                "grounding_dino": "SwinT-OGC",
            },
            metadata={
                "prompts": prompts,
                "box_threshold": box_threshold,
                "text_threshold": text_threshold,
                "num_detections": len(detections),
            },
            created_at=datetime.utcnow(),
        )

        logger.info(
            f"Analysis {analysis_id} completed successfully in {processing_time:.2f}ms "
            f"with {len(detections)} detections"
        )

    except Exception as e:
        logger.error(f"Analysis {analysis_id} failed: {str(e)}", exc_info=True)

        # Update analysis with error
        if analysis_id in analysis_storage:
            analysis_storage[analysis_id].status = AnalysisStatus.FAILED
            analysis_storage[analysis_id].error_message = str(e)


@router.post("/", response_model=AnalysisResponse, status_code=202)
async def create_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    ml_service: MLService = Depends(get_ml_service),
    storage_service: StorageService = Depends(get_storage_service),
) -> AnalysisResponse:
    """
    Create a new image analysis request.

    Args:
        request: Analysis request data
        background_tasks: FastAPI background tasks
        ml_service: ML service instance
        storage_service: Storage service instance

    Returns:
        AnalysisResponse: Initial analysis response with pending status
    """
    try:
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())

        # Get image URL from storage
        image_url = await storage_service.get_image_url(request.image_id)
        if not image_url:
            raise HTTPException(
                status_code=404,
                detail=f"Image {request.image_id} not found"
            )

        # Create initial analysis response
        analysis_response = AnalysisResponse(
            analysis_id=analysis_id,
            image_id=request.image_id,
            status=AnalysisStatus.PENDING,
            detections=[],
            processing_time_ms=0.0,
            metadata={
                "prompts": request.prompts,
                "box_threshold": request.box_threshold,
                "text_threshold": request.text_threshold,
            },
            created_at=datetime.utcnow(),
        )

        # Store initial analysis
        analysis_storage[analysis_id] = analysis_response

        # Add background task for analysis
        background_tasks.add_task(
            run_analysis_task,
            analysis_id=analysis_id,
            image_id=request.image_id,
            image_url=image_url,
            prompts=request.prompts,
            box_threshold=request.box_threshold,
            text_threshold=request.text_threshold,
            include_segmentation=request.include_segmentation,
            ml_service=ml_service,
            storage_service=storage_service,
        )

        logger.info(f"Created analysis request {analysis_id} for image {request.image_id}")

        return analysis_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create analysis: {str(e)}"
        )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str) -> AnalysisResponse:
    """
    Get analysis result by ID.

    Args:
        analysis_id: Unique analysis ID

    Returns:
        AnalysisResponse: Analysis result
    """
    if analysis_id not in analysis_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis {analysis_id} not found"
        )

    return analysis_storage[analysis_id]


@router.get("/image/{image_id}", response_model=List[AnalysisResponse])
async def get_image_analyses(image_id: str) -> List[AnalysisResponse]:
    """
    Get all analyses for a specific image.

    Args:
        image_id: Image ID

    Returns:
        List[AnalysisResponse]: List of analysis results
    """
    analyses = [
        analysis for analysis in analysis_storage.values()
        if analysis.image_id == image_id
    ]

    # Sort by creation time, newest first
    analyses.sort(key=lambda x: x.created_at, reverse=True)

    return analyses


@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: str) -> dict:
    """
    Delete an analysis result.

    Args:
        analysis_id: Unique analysis ID

    Returns:
        dict: Deletion confirmation
    """
    if analysis_id not in analysis_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis {analysis_id} not found"
        )

    del analysis_storage[analysis_id]

    logger.info(f"Deleted analysis {analysis_id}")

    return {"message": f"Analysis {analysis_id} deleted successfully"}
