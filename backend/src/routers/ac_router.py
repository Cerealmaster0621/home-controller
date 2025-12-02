from fastapi import APIRouter, HTTPException
from models.ac_model import (
    ACMode, 
    ACTempControl, 
    ACTimerControl, 
    ACResponse, 
    ACStatusResponse
)
from services.ac_service import (
    ACService,
    ACResourceNotFoundError,
    IRTransmissionError
)

router = APIRouter(prefix="/ac", tags=["ac"])

# Initialize the AC service
ac_service = ACService()

@router.get("/status", response_model=ACStatusResponse)
async def get_ac_status():
    """Get AC status and available controls"""
    return ac_service.get_status()


# ========== MODE CONTROLS - GET ENDPOINTS ==========

@router.get("/aircon/on", response_model=ACResponse)
async def get_aircon_on():
    """Turn on air conditioner (GET)"""
    try:
        result = ac_service.set_ac_mode(ACMode.AIRCON_ON)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heater/on", response_model=ACResponse)
async def get_heater_on():
    """Turn on heater (GET)"""
    try:
        result = ac_service.set_ac_mode(ACMode.HEATER_ON)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/off", response_model=ACResponse)
async def get_ac_off():
    """Turn off AC (GET)"""
    try:
        result = ac_service.set_ac_mode(ACMode.OFF)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== MODE CONTROLS - POST ENDPOINTS ==========

@router.post("/aircon/on", response_model=ACResponse)
async def post_aircon_on():
    """Turn on air conditioner (POST)"""
    try:
        result = ac_service.set_ac_mode(ACMode.AIRCON_ON)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/heater/on", response_model=ACResponse)
async def post_heater_on():
    """Turn on heater (POST)"""
    try:
        result = ac_service.set_ac_mode(ACMode.HEATER_ON)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/off", response_model=ACResponse)
async def post_ac_off():
    """Turn off AC (POST)"""
    try:
        result = ac_service.set_ac_mode(ACMode.OFF)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== TEMPERATURE CONTROLS - GET ENDPOINTS ==========

@router.get("/aircon/temp/up", response_model=ACResponse)
async def get_aircon_temp_up():
    """Increase air conditioner temperature (GET)"""
    try:
        result = ac_service.control_temperature(ACTempControl.AIRCON_TEMP_UP)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heater/temp/up", response_model=ACResponse)
async def get_heater_temp_up():
    """Increase heater temperature (GET)"""
    try:
        result = ac_service.control_temperature(ACTempControl.HEATER_TEMP_UP)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heater/temp/down", response_model=ACResponse)
async def get_heater_temp_down():
    """Decrease heater temperature (GET)"""
    try:
        result = ac_service.control_temperature(ACTempControl.HEATER_TEMP_DOWN)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== TEMPERATURE CONTROLS - POST ENDPOINTS ==========

@router.post("/aircon/temp/up", response_model=ACResponse)
async def post_aircon_temp_up():
    """Increase air conditioner temperature (POST)"""
    try:
        result = ac_service.control_temperature(ACTempControl.AIRCON_TEMP_UP)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/heater/temp/up", response_model=ACResponse)
async def post_heater_temp_up():
    """Increase heater temperature (POST)"""
    try:
        result = ac_service.control_temperature(ACTempControl.HEATER_TEMP_UP)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/heater/temp/down", response_model=ACResponse)
async def post_heater_temp_down():
    """Decrease heater temperature (POST)"""
    try:
        result = ac_service.control_temperature(ACTempControl.HEATER_TEMP_DOWN)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== TIMER CONTROLS - GET ENDPOINTS ==========

@router.get("/timer/on", response_model=ACResponse)
async def get_timer_on():
    """Turn on timer (GET)"""
    try:
        result = ac_service.control_timer(ACTimerControl.TIMER_ON)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timer/up", response_model=ACResponse)
async def get_timer_up():
    """Increase timer (GET)"""
    try:
        result = ac_service.control_timer(ACTimerControl.TIMER_UP)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timer/down", response_model=ACResponse)
async def get_timer_down():
    """Decrease timer (GET)"""
    try:
        result = ac_service.control_timer(ACTimerControl.TIMER_DOWN)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== TIMER CONTROLS - POST ENDPOINTS ==========

@router.post("/timer/on", response_model=ACResponse)
async def post_timer_on():
    """Turn on timer (POST)"""
    try:
        result = ac_service.control_timer(ACTimerControl.TIMER_ON)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/timer/up", response_model=ACResponse)
async def post_timer_up():
    """Increase timer (POST)"""
    try:
        result = ac_service.control_timer(ACTimerControl.TIMER_UP)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/timer/down", response_model=ACResponse)
async def post_timer_down():
    """Decrease timer (POST)"""
    try:
        result = ac_service.control_timer(ACTimerControl.TIMER_DOWN)
        return result
    except ACResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IRTransmissionError as e:
        raise HTTPException(status_code=500, detail=str(e))

