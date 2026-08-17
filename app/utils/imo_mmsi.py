import json
import os
from typing import Dict, Optional
from app.config import CACHE_PATH

class IMOMMSIMapper:
    def __init__(self):
        self.cache: Dict[str, str] = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(CACHE_PATH):
            try:
                with open(CACHE_PATH, 'r') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}

    def save_cache(self):
        with open(CACHE_PATH, 'w') as f:
            json.dump(self.cache, f, indent=2)

    async def get_mmsi(self, imo: str) -> Optional[str]:
        imo = imo.strip()
        if imo in self.cache:
            return self.cache[imo]
        
        # Real API integrate kar sakte ho yahan (VesselAPI etc.)
        known = {"9395044": "368123456", "9234567": "367890123"}
        if imo in known:
            mmsi = known[imo]
            self.cache[imo] = mmsi
            self.save_cache()
            return mmsi
        return None