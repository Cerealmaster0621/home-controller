from pydantic import BaseModel
from enum import Enum


class LightMode(str, Enum):
    ALL_BRIGHT = "all_bright"
    BRIGHT = "bright"
    DARK = "dark"
    OFF = "off"
    ON = "on"


class LightResponse(BaseModel):
    mode: str
    success: bool
    message: str

