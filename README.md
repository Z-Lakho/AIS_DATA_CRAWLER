# Maritime Vessel Crawler

A small FastAPI application that polls AIS (Automatic Identification System) data for a list of vessel IMOs, maps IMOs to MMSIs, stores live vessel state in a CSV, and exposes HTTP endpoints to read that data.

## Features
- Background crawler that periodically polls an AIS data source (AISHub) for ships in `imo_list.csv`.
- Maintains a CSV database of vessels (`data/vessels.csv`).
- Simple IMO→MMSI cache (`data/imo_to_mmsi.json`).
- FastAPI endpoints to list vessels and get vessel details.

## Requirements
- Python 3.9+
- See `requirements.txt` for Python packages (e.g. `fastapi`, `uvicorn`, `aiohttp`, `pandas`).

## Quick start
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create or verify your IMO list at `imo_list.csv` (single column `IMO`).

3. Configure environment variables in a `.env` file or export them:

```
CSV_PATH=data/vessels.csv
CACHE_PATH=data/imo_to_mmsi.json
REFRESH_INTERVAL=60
LOG_LEVEL=INFO
# Provide AISHub username (see note below)
AISHUB_USERNAME=your_aishub_username
```

4. Run the app locally:

```bash
python run.py
```

The service will be available at `http://127.0.0.1:8000/` and the API at `/api`.

## API Endpoints
- `GET /api/vessels` — returns all vessels from the CSV.
- `GET /api/vessel/{imo}` — returns a single vessel by IMO.
- `GET /api/all-live` — returns vessels whose `Status` is `Live`.

## Important notes
- Config mismatch: the code expects an AISHub username variable when fetching data. By default `app/config.py` uses `AISSTREAM_API_KEY`. To fetch from AISHub, set the environment variable `AISHUB_USERNAME` (or update `app/config.py` to match your provider and key names).
- `IMOMMSIMapper` currently contains a small hardcoded mapping and persists lookups to `data/imo_to_mmsi.json`. Replace or extend it with a proper lookup API for production use.
- The crawler writes CSV rows and updates existing IMOs in `data/vessels.csv`.

## Files of interest
- `run.py` — server entrypoint
- `app/main.py` — FastAPI app and background crawler startup
- `app/crawler/ais_crawler.py` — crawler implementation
- `app/api/endpoints.py` — API routes
- `app/utils/imo_mmsi.py` — IMO→MMSI mapper
- `app/models/vessel.py` — Pydantic model for vessel objects

## License
Add a license file if you plan to publish this repository publicly.


