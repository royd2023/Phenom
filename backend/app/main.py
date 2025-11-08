"""
U-CHS Backend - Main Application Entry Point
"""
from fastapi import FastAPI

app = FastAPI(
    title="U-CHS API",
    version="0.1.0",
    description="Universal Crop Health Scanner API",
)

@app.get("/")
async def root():
    return {"message": "U-CHS API - TODO: Implement"}

# TODO: Add CORS middleware
# TODO: Include routers (health, analysis, images, users)
# TODO: Add startup/shutdown events
# TODO: Add global exception handler
