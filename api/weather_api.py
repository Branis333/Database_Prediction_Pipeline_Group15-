from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date, datetime

# PostgreSQL connection settings
PG_CONN = {
    'host': 'aws-0-eu-central-1.pooler.supabase.com',
    'port': 6543,
    'dbname': 'postgres',
    'user': 'postgres.fdmizgsixffqbpbjqdey',
    'password': 'xZ5i6iLA7yZLsJNX'
}

def get_db_connection():
    return psycopg2.connect(**PG_CONN)

app = FastAPI(title="Weather CRUD API")

# Pydantic models
class LocationBase(BaseModel):
    name: str
    state: Optional[str] = None

class Location(LocationBase):
    location_id: int

class ObservationBase(BaseModel):
    location_id: int
    date: date
    min_temp: Optional[float] = None
    max_temp: Optional[float] = None
    rainfall: Optional[float] = None
    humidity_9am: Optional[float] = None
    humidity_3pm: Optional[float] = None
    pressure_9am: Optional[float] = None
    pressure_3pm: Optional[float] = None
    wind_speed_9am: Optional[float] = None
    wind_speed_3pm: Optional[float] = None
    wind_dir_9am: Optional[str] = None
    wind_dir_3pm: Optional[str] = None
    cloud_9am: Optional[float] = None
    cloud_3pm: Optional[float] = None
    temp_9am: Optional[float] = None
    temp_3pm: Optional[float] = None
    rain_today: Optional[bool] = None
    rain_tomorrow: Optional[bool] = None

class Observation(ObservationBase):
    observation_id: int

class PredictionBase(BaseModel):
    observation_id: int
    will_it_rain: bool

class Prediction(PredictionBase):
    prediction_id: int
    predicted_at: datetime

# CRUD endpoints for Locations
@app.post("/locations/", response_model=Location)
def create_location(loc: LocationBase):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO locations (name, state) VALUES (%s, %s) RETURNING location_id, name, state",
        (loc.name, loc.state)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return Location(location_id=row[0], name=row[1], state=row[2])

@app.get("/locations/", response_model=List[Location])
def read_locations():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT location_id, name, state FROM locations")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/locations/{location_id}", response_model=Location)
def read_location(location_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT location_id, name, state FROM locations WHERE location_id = %s",
        (location_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Location not found")
    return Location(location_id=row[0], name=row[1], state=row[2])

@app.put("/locations/{location_id}", response_model=Location)
def update_location(location_id: int, loc: LocationBase):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE locations SET name = %s, state = %s WHERE location_id = %s RETURNING location_id, name, state",
        (loc.name, loc.state, location_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Location not found")
    return Location(location_id=row[0], name=row[1], state=row[2])

@app.delete("/locations/{location_id}", status_code=204)
def delete_location(location_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM locations WHERE location_id = %s", (location_id,))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Location not found")
    conn.commit()
    cur.close()
    conn.close()

# CRUD endpoints for Observations
@app.post("/observations/", response_model=Observation)
def create_observation(obs: ObservationBase):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_observations (
            location_id, date, min_temp, max_temp, rainfall,
            humidity_9am, humidity_3pm, pressure_9am, pressure_3pm,
            wind_speed_9am, wind_speed_3pm, wind_dir_9am,
            wind_dir_3pm, cloud_9am, cloud_3pm, temp_9am, temp_3pm,
            rain_today, rain_tomorrow
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING observation_id
    """, (
        obs.location_id, obs.date, obs.min_temp, obs.max_temp,
        obs.rainfall, obs.humidity_9am, obs.humidity_3pm,
        obs.pressure_9am, obs.pressure_3pm,
        obs.wind_speed_9am, obs.wind_speed_3pm,
        obs.wind_dir_9am, obs.wind_dir_3pm,
        obs.cloud_9am, obs.cloud_3pm, obs.temp_9am,
        obs.temp_3pm, obs.rain_today, obs.rain_tomorrow
    ))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return Observation(observation_id=row[0], **obs.dict())

@app.get("/observations/", response_model=List[Observation])
def read_observations():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT * FROM weather_observations
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/observations/{observation_id}", response_model=Observation)
def read_observation(observation_id: int):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM weather_observations WHERE observation_id = %s", (observation_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Observation not found")
    return row

@app.put("/observations/{observation_id}", response_model=Observation)
def update_observation(observation_id: int, obs: ObservationBase):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE weather_observations SET
            location_id=%s, date=%s, min_temp=%s, max_temp=%s, rainfall=%s,
            humidity_9am=%s, humidity_3pm=%s, pressure_9am=%s, pressure_3pm=%s,
            wind_speed_9am=%s, wind_speed_3pm=%s, wind_dir_9am=%s,
            wind_dir_3pm=%s, cloud_9am=%s, cloud_3pm=%s, temp_9am=%s,
            temp_3pm=%s, rain_today=%s, rain_tomorrow=%s
        WHERE observation_id=%s RETURNING *
    """, (
        obs.location_id, obs.date, obs.min_temp, obs.max_temp,
        obs.rainfall, obs.humidity_9am, obs.humidity_3pm,
        obs.pressure_9am, obs.pressure_3pm, obs.wind_speed_9am,
        obs.wind_speed_3pm, obs.wind_dir_9am, obs.wind_dir_3pm,
        obs.cloud_9am, obs.cloud_3pm, obs.temp_9am, obs.temp_3pm,
        obs.rain_today, obs.rain_tomorrow, observation_id
    ))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Observation not found")
    return Observation(**row)

@app.delete("/observations/{observation_id}", status_code=204)
def delete_observation(observation_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM weather_observations WHERE observation_id = %s", (observation_id,))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Observation not found")
    conn.commit()
    cur.close()
    conn.close()

# CRUD endpoints for Predictions
@app.post("/predictions/", response_model=Prediction)
def create_prediction(pred: PredictionBase):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO rain_predictions (observation_id, will_it_rain) VALUES (%s, %s) RETURNING prediction_id, predicted_at",
        (pred.observation_id, pred.will_it_rain)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return Prediction(prediction_id=row[0], observation_id=pred.observation_id, will_it_rain=pred.will_it_rain, predicted_at=row[1])

@app.get("/predictions/", response_model=List[Prediction])
def read_predictions():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM rain_predictions")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/predictions/{prediction_id}", response_model=Prediction)
def read_prediction(prediction_id: int):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM rain_predictions WHERE prediction_id = %s", (prediction_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return row

@app.put("/predictions/{prediction_id}", response_model=Prediction)
def update_prediction(prediction_id: int, pred: PredictionBase):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE rain_predictions SET observation_id=%s, will_it_rain=%s
        WHERE prediction_id=%s RETURNING prediction_id, observation_id, will_it_rain, predicted_at
    """, (pred.observation_id, pred.will_it_rain, prediction_id))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return Prediction(prediction_id=row[0], observation_id=row[1], will_it_rain=row[2], predicted_at=row[3])

@app.delete("/predictions/{prediction_id}", status_code=204)
def delete_prediction(prediction_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM rain_predictions WHERE prediction_id = %s", (prediction_id,))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Prediction not found")
    conn.commit()
    cur.close()
    conn.close()
