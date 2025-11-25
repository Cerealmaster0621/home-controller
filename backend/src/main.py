from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from routers import light_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Home Controller API",
    description="API for controlling home devices via IR",
    version="1.0.0"
)


# Custom exception classes
class LightResourceNotFoundError(Exception):
    """Raised when a light resource file is not found"""
    pass


class IRTransmissionError(Exception):
    """Raised when IR transmission fails"""
    pass


# Global exception handlers
@app.exception_handler(LightResourceNotFoundError)
async def light_resource_not_found_handler(request: Request, exc: LightResourceNotFoundError):
    logger.error(f"Light resource not found: {exc}")
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
            "error_type": "LightResourceNotFoundError"
        }
    )


@app.exception_handler(IRTransmissionError)
async def ir_transmission_error_handler(request: Request, exc: IRTransmissionError):
    logger.error(f"IR transmission error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "error_type": "IRTransmissionError"
        }
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.error(f"Value error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
            "error_type": "ValueError"
        }
    )


# Include routers
app.include_router(light_router.router)


@app.get("/")
def read_root():
    return {
        "message": "Home Controller API",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "light_control": "/light"
        }
    }

