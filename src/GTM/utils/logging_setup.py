import logging
import sys

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger("gittimemachine")
    logger.setLevel(level)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger