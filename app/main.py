from fastapi import FastAPI
import logging
from app.api.endpoints import router
from app.crawler.ais_crawler import AISCrawler
import asyncio

app = FastAPI(title="Maritime Vessel Crawler")
app.include_router(router, prefix="/api")

crawler = AISCrawler()

@app.on_event("startup")
async def startup():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.create_task(crawler.run())

@app.on_event("shutdown")
def shutdown():
    crawler.stop()

@app.get("/")
def root():
    return {"status": "running"}