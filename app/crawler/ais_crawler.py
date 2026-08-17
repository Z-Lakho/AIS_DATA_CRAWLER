import asyncio
import logging
import os
from datetime import datetime
import pandas as pd
import aiohttp
from typing import List, Dict

from app.config import AISHUB_USERNAME, CSV_PATH, REFRESH_INTERVAL
from app.utils.imo_mmsi import IMOMMSIMapper

logger = logging.getLogger(__name__)

class AISCrawler:
    def __init__(self):
        self.mapper = IMOMMSIMapper()
        self.running = True
        self.mmsi_to_imo: Dict[str, str] = {}

    async def load_imo_list(self) -> List[str]:
        try:
            df = pd.read_csv('imo_list.csv')
            return df['IMO'].astype(str).str.strip().tolist()
        except Exception as e:
            logger.error(f"Failed to load IMO list: {e}")
            return []

    async def init_vessels_csv(self):
        if not os.path.exists(CSV_PATH):
            cols = ['IMO', 'MMSI', 'Vessel Name', 'Vessel Type', 'Flag', 'Latitude', 'Longitude',
                    'Speed_Knots', 'Course', 'Heading', 'Navigation_Status', 'Destination',
                    'ETA', 'Last_Received_UTC', 'Status']
            pd.DataFrame(columns=cols).to_csv(CSV_PATH, index=False)

    async def update_csv(self, vessel_data: Dict):
        try:
            df = pd.read_csv(CSV_PATH)
            imo = str(vessel_data.get('IMO'))
            if imo in df['IMO'].astype(str).values:
                idx = df[df['IMO'].astype(str) == imo].index[0]
                for key, value in vessel_data.items():
                    if key in df.columns:
                        df.at[idx, key] = value
            else:
                df = pd.concat([df, pd.DataFrame([vessel_data])], ignore_index=True)
            df.to_csv(CSV_PATH, index=False)
            logger.info(f"Updated IMO: {imo}")
        except Exception as e:
            logger.error(f"CSV update error: {e}")

    async def fetch_from_aishub(self, mmsis: List[str]):
        if not AISHUB_USERNAME or not mmsis:
            logger.warning("AISHub username missing or no MMSIs")
            return
        try:
            mmsi_str = ','.join(mmsis[:20])  # AISHub limit ke hisaab se
            url = f"https://data.aishub.net/ws.php?username={AISHUB_USERNAME}&format=1&output=json&mmsi={mmsi_str}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        count = len(data) if isinstance(data, list) else 0
                        logger.info(f"AISHub returned {count} vessels")
                        if isinstance(data, list):
                            for vessel in data:
                                await self.process_aishub_vessel(vessel)
        except Exception as e:
            logger.error(f"AISHub fetch failed: {e}")

    async def process_aishub_vessel(self, vessel: Dict):
        try:
            mmsi = str(vessel.get('MMSI', ''))
            if not mmsi or mmsi not in self.mmsi_to_imo:
                return
            imo = self.mmsi_to_imo[mmsi]
            
            vessel_data = {
                'IMO': imo,
                'MMSI': mmsi,
                'Vessel Name': vessel.get('NAME', vessel.get('SHIPNAME', '')),
                'Vessel Type': str(vessel.get('TYPE', '')),
                'Flag': vessel.get('FLAG', ''),
                'Latitude': vessel.get('LATITUDE'),
                'Longitude': vessel.get('LONGITUDE'),
                'Speed_Knots': vessel.get('SPEED'),
                'Course': vessel.get('COURSE'),
                'Heading': vessel.get('HEADING'),
                'Navigation_Status': vessel.get('NAVSTATUS', ''),
                'Destination': vessel.get('DESTINATION', ''),
                'ETA': vessel.get('ETA', ''),
                'Last_Received_UTC': datetime.utcnow().isoformat(),
                'Status': 'Live'
            }
            await self.update_csv(vessel_data)
        except Exception as e:
            logger.error(f"Vessel process error: {e}")

    async def run(self):
        await self.init_vessels_csv()
        while self.running:
            try:
                imos = await self.load_imo_list()
                mmsis = []
                for imo in imos:
                    mmsi = await self.mapper.get_mmsi(imo)
                    if mmsi:
                        mmsis.append(mmsi)
                        self.mmsi_to_imo[mmsi] = imo
                
                await self.fetch_from_aishub(mmsis)
            except Exception as e:
                logger.error(f"Polling error: {e}")
            
            await asyncio.sleep(REFRESH_INTERVAL)

    def stop(self):
        self.running = False