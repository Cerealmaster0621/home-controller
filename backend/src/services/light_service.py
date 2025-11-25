import os
import subprocess
from pathlib import Path
from typing import Dict
from models.light_model import LightMode
from env import IR_CODE_DIR, IR_LIGHT_RESOURCES_PATH, TRANSMITTER_DEVICE


class LightResourceNotFoundError(Exception):
    """Raised when the light resource file is not found"""
    def __init__(self, mode: str):
        self.mode = mode
        super().__init__(f"Light resource file not found for mode: {mode}")


class IRTransmissionError(Exception):
    """Raised when IR transmission fails"""
    def __init__(self, mode: str, details: str):
        self.mode = mode
        self.details = details
        super().__init__(f"Failed to transmit IR signal for mode '{mode}': {details}")


class LightService:
    def __init__(self):
        self.ir_code_dir = IR_CODE_DIR
        self.resources_path = IR_LIGHT_RESOURCES_PATH
        self.transmitter_device = TRANSMITTER_DEVICE
        
        # Validate environment variables
        if not self.resources_path:
            raise ValueError("IR_LIGHT_RESOURCES_PATH environment variable is not set")
        if not self.ir_code_dir:
            raise ValueError("IR_CODE_DIR environment variable is not set")
        if not self.transmitter_device:
            raise ValueError("transmitter_device environment variable is not set")
    
    def _get_resource_file_path(self, mode: LightMode) -> Path:
        """Get the full path to the light resource file"""
        filename = f"light_{mode.value}.txt"
        file_path = Path(self.resources_path) / filename
        
        if not file_path.exists():
            raise LightResourceNotFoundError(mode.value)
        
        return file_path
    
    def _transmit_ir_signal(self, resource_file: Path) -> None:
        """Transmit IR signal using the resource file"""
        try:
            # Validate that the resource file exists
            if not resource_file.exists():
                raise IRTransmissionError(
                    resource_file.stem,
                    "IR code file not found"
                )
            
            # ir-ctl command: -d for device, --send for file transmission
            cmd = [
                "ir-ctl",
                "-d", self.transmitter_device,
                "--send", str(resource_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
                
        except subprocess.TimeoutExpired:
            raise IRTransmissionError(
                resource_file.stem,
                "IR transmission timed out"
            )
        except subprocess.CalledProcessError as e:
            raise IRTransmissionError(
                resource_file.stem,
                f"Command failed with code {e.returncode}: {e.stderr}"
            )
        except FileNotFoundError as e:
            raise IRTransmissionError(
                resource_file.stem,
                f"IR transmission command not found: {str(e)}"
            )
        except Exception as e:
            if isinstance(e, IRTransmissionError):
                raise
            raise IRTransmissionError(
                resource_file.stem,
                f"Unexpected error: {str(e)}"
            )
    
    def set_light_mode(self, mode: LightMode) -> Dict[str, any]:
        """
        Set the light to a specific mode
        
        Raises:
            LightResourceNotFoundError: If the resource file doesn't exist
            IRTransmissionError: If IR transmission fails
        """
        resource_file = self._get_resource_file_path(mode)
        self._transmit_ir_signal(resource_file)
        
        return {
            "mode": mode.value,
            "success": True,
            "message": f"Light set to {mode.value} mode successfully"
        }
    
    def get_available_modes(self) -> list[str]:
        """Get list of available light modes"""
        return [mode.value for mode in LightMode]

