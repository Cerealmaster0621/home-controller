from dotenv import load_dotenv
import os

load_dotenv()

IR_CODE_DIR = os.getenv('IR_CODE_DIR')
IR_LIGHT_RESOURCES_PATH = os.getenv('IR_LIGHT_RESOURCES_PATH')
IR_AC_RESOURCES_PATH = os.getenv('IR_AC_RESOURCES_PATH')
TRANSMITTER_DEVICE = os.getenv('TRANSMITTER_DEVICE')
RECEIVER_DEVICE = os.getenv('RECEIVER_DEVICE')