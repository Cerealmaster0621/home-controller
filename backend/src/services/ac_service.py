import os
import subprocess
from pathlib import Path
from typing import Dict, Union
from models.ac_model import ACMode, ACTempControl, ACTimerControl
from env import IR_CODE_DIR, IR_AC_RESOURCES_PATH, TRANSMITTER_DEVICE


class ACResourceNotFoundError(Exception):
    """Raised when the AC resource file is not found"""
    def __init__(self, action: str):
        self.action = action
        super().__init__(f"AC resource file not found for action: {action}")


class IRTransmissionError(Exception):
    """Raised when IR transmission fails"""
    def __init__(self, action: str, details: str):
        self.action = action
        self.details = details
        super().__init__(f"Failed to transmit IR signal for action '{action}': {details}")


class ACService:
    def __init__(self):
        self.ir_code_dir = IR_CODE_DIR
        self.resources_path = IR_AC_RESOURCES_PATH
        self.transmitter_device = TRANSMITTER_DEVICE
        
        # Validate environment variables
        if not self.resources_path:
            raise ValueError("IR_AC_RESOURCES_PATH environment variable is not set")
        if not self.ir_code_dir:
            raise ValueError("IR_CODE_DIR environment variable is not set")
        if not self.transmitter_device:
            raise ValueError("TRANSMITTER_DEVICE environment variable is not set")
    
    def _get_resource_file_path(self, action: Union[ACMode, ACTempControl, ACTimerControl]) -> Path:
        """Get the full path to the AC resource file"""
        filename = f"ac_{action.value}.txt"
        file_path = Path(self.resources_path) / filename
        
        if not file_path.exists():
            raise ACResourceNotFoundError(action.value)
        
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
    
    def set_ac_mode(self, mode: ACMode) -> Dict[str, any]:
        """
        Set the AC to a specific mode (aircon on, heater on, or off)
        
        Raises:
            ACResourceNotFoundError: If the resource file doesn't exist
            IRTransmissionError: If IR transmission fails
        """
        resource_file = self._get_resource_file_path(mode)
        self._transmit_ir_signal(resource_file)
        
        return {
            "action": mode.value,
            "success": True,
            "message": f"AC set to {mode.value} mode successfully"
        }
    
    def control_temperature(self, control: ACTempControl) -> Dict[str, any]:
        """
        Control AC temperature
        
        Raises:
            ACResourceNotFoundError: If the resource file doesn't exist
            IRTransmissionError: If IR transmission fails
        """
        resource_file = self._get_resource_file_path(control)
        self._transmit_ir_signal(resource_file)
        
        return {
            "action": control.value,
            "success": True,
            "message": f"Temperature control {control.value} executed successfully"
        }
    
    def control_timer(self, control: ACTimerControl) -> Dict[str, any]:
        """
        Control AC timer
        
        Raises:
            ACResourceNotFoundError: If the resource file doesn't exist
            IRTransmissionError: If IR transmission fails
        """
        resource_file = self._get_resource_file_path(control)
        self._transmit_ir_signal(resource_file)
        
        return {
            "action": control.value,
            "success": True,
            "message": f"Timer control {control.value} executed successfully"
        }
    
    def get_available_modes(self) -> list[str]:
        """Get list of available AC modes"""
        return [mode.value for mode in ACMode]
    
    def get_available_temp_controls(self) -> list[str]:
        """Get list of available temperature controls"""
        return [control.value for control in ACTempControl]
    
    def get_available_timer_controls(self) -> list[str]:
        """Get list of available timer controls"""
        return [control.value for control in ACTimerControl]
    
    def get_status(self) -> Dict[str, list[str]]:
        """Get all available AC controls"""
        return {
            "available_modes": self.get_available_modes(),
            "available_temp_controls": self.get_available_temp_controls(),
            "available_timer_controls": self.get_available_timer_controls()
        }

