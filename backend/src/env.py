   from dotenv import load_dotenv
   import os

   load_dotenv()

   IR_CODE_DIR = os.getenv('IR_CODE_DIR')
   IR_LIGHT_RESOURCES_PATH = os.getenv('IR_LIGHT_RESOURCES_PATH')
   TX_DEVICE = os.getenv('TX_DEVICE')