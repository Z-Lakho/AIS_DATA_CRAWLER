import uvicorn
import logging
from app.config import LOG_LEVEL

if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)