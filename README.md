# 🌊 Hydrological Data Engineering Pipeline (Pantanal Biome)

**Author:** Ana Paula Leão
**Master's Thesis Project:** Predicting Droughts in the Miranda River Basin using LSTMs.

---

## 🎯 Project Overview

This repository hosts an End-to-End Data Engineering pipeline built to process hydrological data from the **Brazilian National Water Agency (ANA)**. The focus is monitoring the **Miranda River Basin**, a critical region in the Pantanal Biome.

The project implements a **Robust Hybrid Architecture** designed for reliability:

1.  **Resilient Ingestion (Bronze):** A smart extraction engine that prioritizes the official API but automatically switches to a **Manual Fallback Mechanism** if the API fails or returns incomplete data.
2.  **Trusted Transformation (Silver):** Advanced data cleaning pipeline with **Data Lineage tracking**, strictly enforcing daily continuity and removing statistical noise.

---

## 🚀 Project Roadmap & Status

### Phase 1: Ingestion (Bronze Layer) ✅ _Completed_

- [x] **Hybrid Extraction Engine:** Logic to prioritize API (`hydrobr`) but automatically fallback to local CSV snapshots if the API is unstable.
- [x] **Resilience Patterns:** Implementation of a custom **Retry Decorator with Exponential Backoff** to handle transient network failures.
- [x] **Locale-Aware Parsing:** engineered a robust parser to handle **Brazilian CSV formats** (semicolon delimiters `;` and decimal commas `,`), implementing a "Nuclear Fix" strategy to prevent data loss (`NaN`) during type conversion.
- [x] **Data Lineage:** Tagging every record with a `data_origin` metadata field (API vs. MANUAL) for full auditability.

### Phase 2: Transformation (Silver Layer) ✅ _Completed_

- [x] **Defensive Programming:** Implementation of strict column sanitization (Regex) and **Blacklisting** logic to remove "ghost" stations.
- [x] **Quality Gates:** Automated audit system that flags stations with **>10% missing data** as "High Risk".
- [x] **Gap Filling:** Application of **Linear Interpolation** to preserve the physical continuity of river flow trends.
- [x] **Storage Optimization:** Migration from CSV to **Parquet** (Snappy compression) for type safety and performance.

### Phase 3: Feature Engineering (Gold Layer) 🚧 _Next Step_

- [ ] **Normalization:** Applying `MinMaxScaler` (0-1) to ensure LSTM convergence.
- [ ] **Windowing:** Creating sliding windows (lag features) for time-series forecasting.
- [ ] **Train/Test Split:** Segregating data using a time-based split to prevent look-ahead bias.

### Phase 4: Production & MLOps 🔮 _Future Release_

- [ ] **Dockerization:** Containerizing the ETL scripts (`Dockerfile`) for reproducibility.
- [ ] **CI/CD:** Setting up GitHub Actions for automated linting and testing.

---

## 📂 Repository Structure

```text
.
├── notebooks_analysis/
│   ├── 01_Bronze_Ingestion.ipynb      <-- (Extraction & Fallback Logic)
│   └── 02_Silver_Transformation.ipynb <-- (Quality Gates & Parquet)
│
├── datalake_simulated/                <-- Local Data Lake Structure
│   ├── manual_upload/                 <-- Place your manual .csv backups here
│   ├── raw/                           <-- Bronze Layer Output (CSVs)
│   └── silver/                        <-- Silver Layer Output (Parquet)
│
├── docs/
│   └── SILVER_DESIGN.md               <-- Technical Design Decisions
│
└── README.md
```

## 🛠️ Technical Deep Dive: The Ingestion Challenge

One of the critical challenges in this project was handling the heterogeneity of hydrological data sources.

- **The Problem:** Manual backup files from Brazilian agencies often use **Decimal Commas** (`12,5`) instead of dots, and varied delimiters (`;` or `\t`). Standard libraries often fail to parse this, resulting in null values.
- **The Solution:** I implemented a **Multi-Strategy Parser** in the Bronze Layer that:
  1.  Detects the delimiter automatically.
  2.  Treats all columns as strings initially to preserve integrity.
  3.  Applies a vectorized replacement of commas to dots.
  4.  Coerces data to `Float64` only after sanitization.
