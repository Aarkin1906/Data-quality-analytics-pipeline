# 📊 Data Quality & YouTube Analytics Pipeline

An end-to-end Data Quality, Processing, and OLAP Analytics Pipeline built with **Python**, **DuckDB**, and **Streamlit**.

---

## 📌 Project Overview
This project ingests raw YouTube Video analytics data, executes automated data quality audits, cleans and standardizes the dataset, stores it in an in-memory **DuckDB** OLAP database, and renders interactive analytical visual reports.

---

## 🎯 Key Features & Requirements Met
- **Data Ingestion**: Ingests raw CSV data into a Python environment.
- **Data Quality Audit**:
  - Deduplication via `video_id`.
  - Null/NaN missing value handling.
  - Filtering negative/invalid metrics (views/likes validation).
  - Schema and data type standardization.
- **DuckDB Integration**: Columnar OLAP engine for high-speed analytical SQL queries.
- **Interactive Dashboard**:
  - Dynamic category sidebar filter and live title search bar.
  - KPI overview metrics (Total Videos, Views, Likes, Engagement Rate).
  - Plotly interactive charts & top-performing video leaderboards.

---

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Data Processing**: Pandas, Faker
- **Database (OLAP)**: DuckDB
- **Visualization**: Streamlit, Plotly

---

## 🚀 How to Run the Project Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt