# 🌊 HydroPipeline: Resilient Hydrological Data Ingestion

[![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)](https://www.python.org/)
[![Azure](https://img.shields.io/badge/Cloud-Azure_Blob_Storage-0078D4?logo=microsoft-azure)](https://azure.microsoft.com/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Project Overview

This project implements an **End-to-End Data Engineering Pipeline** designed to ingest, process, and analyze historical hydrological data from the **Brazilian National Water Agency (ANA)**.

Developed as part of a Master's Thesis in Water Resources Management, the system monitors the **Miranda River Basin (Pantanal Biome)**, a critical region subject to extreme drought and flood events. The architecture ensures high availability and data integrity for downstream predictive modeling (LSTM/Deep Learning).

### 🎯 Key Objectives

- **Resilience:** Overcome public API instabilities using `Retry` patterns with exponential backoff.
- **Scalability:** Modular architecture ready for high-volume ingestion.
- **Cloud-Native:** Automated integration with **Microsoft Azure Blob Storage** (Data Lake Gen2).
- **Reproducibility:** Fully containerized environment using **Docker**.

---

## 🏗️ Architecture

The project follows the **Medallion Architecture** (Lakehouse pattern) to organize data quality levels:

| Layer                   |    Status    | Description                                                                                                   |
| :---------------------- | :----------: | :------------------------------------------------------------------------------------------------------------ |
| **🥉 Bronze (Raw)**     | ✅ **Done**  | Raw data ingestion from API to Azure Blob Storage (CSV format). Preserves original history with partitioning. |
| **🥈 Silver (Refined)** | 🚧 _Planned_ | Data cleaning, deduplication, and gap filling (Imputation). Conversion to Parquet format using Spark.         |
| **🥇 Gold (Curated)**   | 🚧 _Planned_ | Aggregations and Feature Engineering (Lags, Moving Averages) for the Machine Learning model.                  |

### 📂 Directory Structure

The codebase follows a modular design pattern to ensure separation of concerns:

```text
azure-hydro-pipeline/
├── data/                   # Local data landing zone (gitignored)
├── notebooks/              # Jupyter Notebooks for EDA and Visual Validation
├── src/                    # Source Code
│   ├── etl/
│   │   └── bronze/         # Bronze Layer specific logic
│   │       ├── extraction.py
│   │       └── loading.py
│   ├── config.py           # Global settings & Decorators
│   └── main.py             # Pipeline Orchestrator
├── Dockerfile              # Container definition
├── .env                    # Environment variables (gitignored)
└── requirements.txt        # Python dependencies
```

---

## 🛠️ Tech Stack & Concepts

- **Language:** Python 3.9+
- **Cloud:** Microsoft Azure Blob Storage (Containers & Partitioning)
- **Containerization:** Docker & Azure Container Instances (ACI)
- **Libraries:** `Pandas`, `HydroBr`, `Azure-Storage-Blob`, `Python-Dotenv`
- **Design Patterns:** OOP, Singleton (Config), Decorators (Retry Logic), Separation of Concerns.

---

## 🚀 How to Run

### Prerequisites

- Docker installed
- Azure Storage Account (Connection String)

### Option 1: Running with Docker (Recommended)

1. **Build the Image:**
   ```bash
   docker build -t hydro-pipeline .
   ```

## 🚀 Usage

You can run the pipeline either using Docker or locally with Python.

### Option 1: Running with Docker

Pass the connection string as an environment variable to ensure security.

```bash
docker run -e AZURE_CONNECTION_STRING="your_connection_string_here" hydro-pipeline
```

### Option 2: Running Locally (Python)

**1. Install Dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure Environment**

Create a `.env` file in the root directory and add your Azure credentials:

```plaintext
AZURE_CONNECTION_STRING="your_connection_string_here"
```

**3. Execute the Pipeline**

```bash
python -m src.main
```

---

## 📊 Data Partitioning Strategy

To optimize storage and retrieval in the Data Lake, raw data is saved using **Hive-Style Partitioning**.

**Structure Overview:**

```plaintext
container: hidropipeline-raw
└── ana (Source System)
    ├── flow (Entity)
    │   └── load_date=2026-01-24 (Partition)
    │       └── thesis_flow_data.csv
    └── rainfall (Entity)
        └── load_date=2026-01-24 (Partition)
            └── thesis_rainfall_data.csv
```

---

## 📈 Visual Validation

The repository includes a validation notebook to inspect the integrity of the downloaded time series, ensuring there are no corrupted files before the transformation stage.

- **Location:** `notebooks/visual_validation.ipynb`

---

## 👤 Author

**Ana Paula Leão**
_Data Engineer & Researcher_
