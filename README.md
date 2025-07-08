# Weather Data Database & API Project

## Overview
This project demonstrates a weather data pipeline using both PostgreSQL (Supabase) and MongoDB, with FastAPI endpoints and scripts for data import and ML preparation.

## Features
- Relational schema (PostgreSQL/Supabase) and NoSQL schema (MongoDB)
- Data import from `weatherAUS.csv` (supports large files, chunked inserts)
- FastAPI app for API endpoints
- ERD diagram (see `weather_erd.dbml`)

## Setup

### 1. Install Requirements
```
pip install -r requirements.txt
```

### 2. Configure Database Connections
- Edit `import_weather_data.py` and `weather_api.py` with your Supabase and MongoDB connection details if needed.

### 3. Import Data
```
python import_weather_data.py
```
- By default, loads 25,000 rows from `weatherAUS.csv` (edit `nrows` in the script to change).

### 4. Generate ERD Image
- Upload `weather_erd.dbml` to [dbdiagram.io](https://dbdiagram.io/) and export as PNG or PDF.

### 5. Run FastAPI App
```
uvicorn weather_api:app --reload
```
- Access docs at http://127.0.0.1:8000/docs

## Files
- `import_weather_data.py` — Data import script
- `weather_api.py` — FastAPI app
- `weather_erd.dbml` — ERD diagram source
- `requirements.txt` — Python dependencies
- `weatherAUS.csv` — Weather dataset

## Notes
- For large imports, chunk size can be adjusted in the scripts.
- Make sure your databases are running and accessible before importing data.

---

**Author:** Group 15
## ERD IMAGE

![Weather ERD][imageRef]

[imageRef]: Untitled.png