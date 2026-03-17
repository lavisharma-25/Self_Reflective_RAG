import os
import uvicorn
import webbrowser

from app.config import port
from logs import setup_logger

logger = setup_logger()

if __name__ == "__main__":
    url = f"http://127.0.0.1:{port}"
    logger.info(f"Server running at: {url}")

    webbrowser.open(url)
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)