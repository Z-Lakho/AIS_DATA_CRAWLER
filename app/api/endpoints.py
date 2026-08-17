from fastapi import APIRouter, HTTPException
import pandas as pd
from typing import List
from app.models.vessel import Vessel
from app.config import CSV_PATH

router = APIRouter()

@router.get("/vessels", response_model=List[Vessel])
async def get_vessels():
    try:
        df = pd.read_csv(CSV_PATH)
        return df.to_dict(orient='records')
    except:
        return []

@router.get("/vessel/{imo}", response_model=Vessel)
async def get_vessel(imo: str):
    try:
        df = pd.read_csv(CSV_PATH)
        row = df[df['IMO'].astype(str) == imo]
        if row.empty:
            raise HTTPException(404, "Vessel not found")
        return row.iloc[0].to_dict()
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/all-live")
async def get_live():
    try:
        df = pd.read_csv(CSV_PATH)
        return df[df['Status'] == 'Live'].to_dict(orient='records')
    except:
        return []