# config/logger.py
import logging
from pathlib import Path

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=log_dir / "app.log",
        level=logging.WARNING,  # Set to WARNING or ERROR to suppress INFO logs
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger(__name__)
