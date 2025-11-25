from pydantic import BaseModel
from enum import Enum


class ACMode(str, Enum):
    AIRCON_ON = "aircon_on"
    HEATER_ON = "heater_on"
    OFF = "off"


class ACTempControl(str, Enum):
    AIRCON_TEMP_UP = "aircon_temp_up"
    HEATER_TEMP_UP = "heater_temp_up"
    HEATER_TEMP_DOWN = "heater_temp_down"


class ACTimerControl(str, Enum):
    TIMER_ON = "timer_on"
    TIMER_UP = "timer_up"
    TIMER_DOWN = "timer_down"


class ACResponse(BaseModel):
    action: str
    success: bool
    message: str


class ACStatusResponse(BaseModel):
    available_modes: list[str]
    available_temp_controls: list[str]
    available_timer_controls: list[str]

