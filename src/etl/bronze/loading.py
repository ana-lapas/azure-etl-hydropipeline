import pandas as pd
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from src.config import PipelineConfig

class DataLoader:
    """Handles data persistence strategy (Local Disk + Azure Blob Storage)."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.blob_service_client = None
        if self.config.azure_conn_string:
            try:
                self.blob_service_client = BlobServiceClient.from_connection_string(self.config.azure_conn_string)
                logging.info("☁️ Azure Blob Storage client initialized.")
            except Exception as e:
                logging.error(f"⚠️ Failed to connect to Azure: {e}")

    def _filter_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty: return df
        logging.info(f"✂️ Filtering data between {self.config.start_date} and {self.config.end_date}...")
        return df.loc[self.config.start_date : self.config.end_date]

    def save_data(self, df: pd.DataFrame, entity_name: str, filename: str):
        if df is None or df.empty:
            logging.warning(f"⏩ No data to save for {filename}.")
            return

        # 1. Transformation
        df_filtered = self._filter_by_date(df)

        # 2. Local Save
        # Note: Local path doesn't need partition for simplicity in Bronze, 
        # but Cloud needs it.
        local_path = self.config.raw_path / entity_name
        full_local_path = local_path / filename
        df_filtered.to_csv(full_local_path)
        logging.info(f"💾 [LOCAL] File saved: {full_local_path}")

        # 3. Cloud Upload (With Partitioning)
        current_date = datetime.now().strftime("%Y-%m-%d")
        partition_path = f"load_date={current_date}"
        blob_path = f"ana/{entity_name}/{partition_path}/{filename}"

        if self.blob_service_client:
            try:
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.config.azure_container_name, 
                    blob=blob_path
                )
                logging.info(f"☁️ [AZURE] Uploading to: {blob_path}")
                blob_client.upload_blob(df_filtered.to_csv(index=True), overwrite=True)
                logging.info(f"✅ [AZURE] Success.")
            except Exception as e:
                logging.error(f"❌ [AZURE] Upload failed: {e}")