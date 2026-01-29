# 🌊 Hydrological Data Engineering Pipeline (Pantanal Biome)

**Author:** Ana Paula Leão
**Master's Thesis Project:** Predicting Droughts in the Miranda River Basin using LSTMs.

---

## 🎯 Project Overview

This repository hosts the Data Engineering pipeline built to process hydrological data from the **Brazilian National Water Agency (ANA)**. The focus is monitoring the **Miranda River Basin**, a critical region in the Pantanal Biome.

The project follows a **Hybrid Architecture**:

1.  **Cloud Ingestion (Azure):** Automated Python scripts for resilient extraction (Bronze Layer).
2.  **Analytical Transformation:** Jupyter Notebooks for data cleaning, gap filling (Silver Layer), and exploratory analysis.

---

## 🚀 Project Roadmap & Status

### Phase 1: Ingestion (Bronze Layer) ✅ _Current Release_

- [x] **Resilient API Connection:** Implementation of Retry Pattern to handle ANA API instability.
- [x] **Raw Data Extraction:** Automated download of Flow and Rainfall historical data (1994-2024).
- [x] **Bronze Notebook Demo:** Interactive documentation of the ingestion process.

### Phase 2: Transformation (Silver Layer) 🚧 _In Progress_

- [ ] **Temporal Alignment:** Reindexing to ensure a consistent daily calendar (handling missing dates).
- [ ] **Gap Filling:** Implementation of Linear Interpolation for hydrological continuity.
- [ ] **Parquet Conversion:** Optimization for columnar storage and strict typing.

### Phase 3: Feature Engineering (Gold Layer) 🔮 _Planned_

- [ ] **Normalization:** Applying `MinMaxScaler` (0-1) to ensure LSTM convergence.
- [ ] **Windowing:** Creating sliding windows (lag features) for time-series forecasting.
- [ ] **Train/Test Split:** Segregating data to prevent look-ahead bias and data leakage.

### Phase 4: DevOps & MLOps 🔮 _Future Release_

- [ ] **Dockerization:** Containerizing the ETL scripts (`Dockerfile`) to ensure reproducibility across environments.
- [ ] **CI/CD Pipelines:** Setting up GitHub Actions for automated testing and linting.

---

## 📂 Repository Structure

```text
.
├── notebooks_analysis/
│   └── 01_Bronze_Ingestion_Demo.ipynb  <-- START HERE (Active)
│
├── src_azure_ingestion/                <-- (Pending Upload)
└── README.md
```
