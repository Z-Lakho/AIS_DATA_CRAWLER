import os
from dotenv import load_dotenv

load_dotenv()

AISSTREAM_API_KEY = os.getenv("AISSTREAM_API_KEY")
CSV_PATH = os.getenv("CSV_PATH", "data/vessels.csv")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
RECONNECT_DELAY = int(os.getenv("RECONNECT_DELAY", 5))
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 60))
CACHE_PATH = os.getenv("CACHE_PATH", "data/imo_to_mmsi.json")

os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)