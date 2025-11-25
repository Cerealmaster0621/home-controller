import os
import subprocess
from pathlib import Path
from typing import Dict
from models.light_model import LightMode
from env import IR_CODE_DIR, IR_LIGHT_RESOURCES_PATH, TX_DEVICE


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
        self.tx_device = TX_DEVICE
        
        # Validate environment variables
        if not self.resources_path:
            raise ValueError("IR_LIGHT_RESOURCES_PATH environment variable is not set")
        if not self.ir_code_dir:
            raise ValueError("IR_CODE_DIR environment variable is not set")
        if not self.tx_device:
            raise ValueError("TX_DEVICE environment variable is not set")
    
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
            # Read the IR code from the resource file
            with open(resource_file, 'r') as f:
                ir_code = f.read().strip()
            
            if not ir_code:
                raise IRTransmissionError(
                    resource_file.stem,
                    "IR code file is empty"
                )
            
            # Execute IR transmission command
            # Adjust this command based on your actual IR transmission setup
            cmd = [
                os.path.join(self.ir_code_dir, "ir_send"),  # or your actual IR command
                "-d", self.tx_device,
                ir_code
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                raise IRTransmissionError(
                    resource_file.stem,
                    f"Command failed with code {result.returncode}: {result.stderr}"
                )
                
        except subprocess.TimeoutExpired:
            raise IRTransmissionError(
                resource_file.stem,
                "IR transmission timed out"
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

