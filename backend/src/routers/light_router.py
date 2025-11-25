from fastapi import APIRouter, HTTPException
from models.light_model import LightMode, LightResponse
from services.light_service import (
    LightService,
    LightResourceNotFoundError,
    IRTransmissionError
)

router = APIRouter(prefix="/light", tags=["light"])

# Initialize the light service
light_service = LightService()


@router.get("/modes", response_model=list[str])
async def get_available_modes():
    """Get list of available light modes"""
    return light_service.get_available_modes()


@router.get("/all-bright", response_model=LightResponse)
async def set_light_all_bright():
    """Set light to all bright mode"""
    try:
        result = light_service.set_light_mode(LightMode.ALL_BRIGHT)
        return result
    except LightResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bright", response_model=LightResponse)
async def set_light_bright():
    """Set light to bright mode"""
    try:
        result = light_service.set_light_mode(LightMode.BRIGHT)
        return result
    except LightResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dark", response_model=LightResponse)
async def set_light_dark():
    """Set light to dark mode"""
    try:
        result = light_service.set_light_mode(LightMode.DARK)
        return result
    except LightResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/off", response_model=LightResponse)
async def set_light_off():
    """Turn light off"""
    try:
        result = light_service.set_light_mode(LightMode.OFF)
        return result
    except LightResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/on", response_model=LightResponse)
async def set_light_on():
    """Turn light on"""
    try:
        result = light_service.set_light_mode(LightMode.ON)
        return result
    except LightResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))

