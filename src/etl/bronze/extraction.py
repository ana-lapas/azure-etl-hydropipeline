import hydrobr
import pandas as pd
import logging
from typing import List, Optional
from src.config import PipelineConfig, retry_with_backoff

class ANAExtractor:
    """Handles communication with the National Water Agency (ANA) API."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self._setup_environment()

    def _setup_environment(self):
        """Ensures local directory structure exists."""
        (self.config.raw_path / "flow").mkdir(parents=True, exist_ok=True)
        (self.config.raw_path / "rainfall").mkdir(parents=True, exist_ok=True)

    @retry_with_backoff(max_attempts=3, delay=5)
    def _fetch_from_api(self, fetch_func, codes: List[str], data_type_name: str) -> pd.DataFrame:
        logging.info(f"📡 Starting download for {len(codes)} {data_type_name} stations...")
        df = fetch_func(codes)
        if df is None or df.empty:
            logging.warning(f"⚠️ API returned empty data for {data_type_name}.")
        else:
            logging.info(f"✅ Success: Retrieved {len(df)} records for {data_type_name}.")
        return df

    def run_flow_extraction(self) -> Optional[pd.DataFrame]:
        return self._fetch_from_api(
            hydrobr.get_data.ANA.flow_data,
            self.config.flow_stations,
            "FLOW"
        )

    def run_rain_extraction(self) -> Optional[pd.DataFrame]:
        return self._fetch_from_api(
            hydrobr.get_data.ANA.prec_data,
            self.config.rain_stations,
            "RAINFALL"
        )