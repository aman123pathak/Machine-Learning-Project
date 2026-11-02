import logging
import os
from datetime import datetime
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOGS_PATH = PROJECT_ROOT / "logs"
LOGS_PATH.mkdir(parents=True, exist_ok=True)

LOG_FILE_PATH = LOGS_PATH / LOG_FILE

logging.basicConfig(
    filename=str(LOG_FILE_PATH),
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    encoding="utf-8"
)

if __name__=="__main__":
    logging.info("Logging has started")