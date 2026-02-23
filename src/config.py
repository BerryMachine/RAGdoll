import os
from dotenv import load_dotenv

load_dotenv("local.env")

TESSDATA_PREFIX = os.getenv("TESSDATA_PREFIX")
TORCH_DEVICE = os.getenv("TORCH_DEVICE")
INFERENCE_RAM = int(os.getenv("INFERENCE_RAM"))