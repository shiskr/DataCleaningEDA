# 🚀 Automated Data Pipeline with EDA

An end-to-end data pipeline that ingests CSV or Excel files, cleans data,
performs feature engineering, and generates automated EDA reports.

## 🔧 Features
- CSV & XLSX support
- Schema validation
- Data cleaning
- Feature engineering
- Automated EDA (HTML report)
- Dockerized execution

## 🧱 Architecture
Input → Clean → Feature Engineering → EDA → Output

## 📦 Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- YData Profiling
- Docker

## ▶ How to Run
```bash
docker build -t data-pipeline .
docker run -v $(pwd)/input:/app/input \
           -v $(pwd)/output:/app/output \
           data-pipeline