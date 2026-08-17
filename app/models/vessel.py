from pydantic import BaseModel
from typing import Optional

class Vessel(BaseModel):
    IMO: str
    MMSI: Optional[str] = None
    Vessel_Name: Optional[str] = None
    Vessel_Type: Optional[str] = None
    Flag: Optional[str] = None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    Speed_Knots: Optional[float] = None
    Course: Optional[float] = None
    Heading: Optional[float] = None
    Navigation_Status: Optional[str] = None
    Destination: Optional[str] = None
    ETA: Optional[str] = None
    Last_Received_UTC: Optional[str] = None
    Status: Optional[str] = None