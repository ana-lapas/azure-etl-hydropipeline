import os
from pathlib import Path
from dotenv import load_dotenv
from src_azure_ingestion.config import PipelineConfig
from src_azure_ingestion.extraction import ANAExtractor
from src_azure_ingestion.loading import DataLoader

# Load the .env file
load_dotenv()

# Entry Point
if __name__ == "__main__":
    print("\n--- 🌎 STARTING HYBRID PIPELINE (LOCAL + AZURE) ---")
    
    # Configuration
    # In production, use: os.getenv("AZURE_CONN_STRING")
    AZURE_STR = os.getenv("AZURE_CONNECTION_STRING")
    if not AZURE_STR:
        raise ValueError("❌ Erro: A variável de ambiente AZURE_CONNECTION_STRING não foi definida.")
    
    config = PipelineConfig(
        flow_stations=['66945000', '66941000', '66926000'],
        rain_stations=['1954002', '2054005', '2054019'],
        raw_path=Path("./data/raw"),
        azure_conn_string=AZURE_STR
    )

    # Initialize Services
    extractor = ANAExtractor(config)
    loader = DataLoader(config)

    # Execution Flow
    try:
        # 1. Flow Data
        df_flow = extractor.run_flow_extraction()
        loader.save_data(df_flow, "flow", "thesis_flow_data.csv")

        # 2. Rainfall Data
        df_rain = extractor.run_rain_extraction()
        loader.save_data(df_rain, "rainfall", "thesis_rainfall_data.csv")
        
        print("\n🏁 Pipeline finished successfully.")
        
    except Exception as e:
        print(f"\n🔥 Critical Pipeline Failure: {e}")
        exit(1)