import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from functools import wraps

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

@dataclass(frozen=True)
class PipelineConfig:
    """Immutable Configuration for the ETL Pipeline."""
    flow_stations: List[str]
    rain_stations: List[str]
    raw_path: Path
    start_date: str = '1994-02-01'
    end_date: str = '2024-01-31'
    azure_conn_string: Optional[str] = None
    azure_container_name: str = "hidropipeline-raw"
    max_retries: int = 3
    retry_delay_seconds: int = 5

def retry_with_backoff(max_attempts: int, delay: int):
    """Decorator to retry failed operations with a delay."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"⚠️ Attempt {attempt}/{max_attempts} failed for '{func.__name__}': {e}")
                    if attempt == max_attempts:
                        logging.error(f"❌ All {max_attempts} attempts failed.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator