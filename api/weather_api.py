from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date, datetime
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import PyMongoError
from fastapi.exceptions import RequestValidationError

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

app = FastAPI(title="Rainfall Prediction API")

# Exception handlers for robust error handling
@app.exception_handler(psycopg2.Error)
async def postgres_exception_handler(request: Request, exc: psycopg2.Error):
    return JSONResponse(status_code=500, content={"detail": "PostgreSQL error", "error": str(exc)})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})

# Handle HTTPException separately to preserve status codes
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# MongoDB error handler
@app.exception_handler(PyMongoError)
async def mongo_exception_handler(request: Request, exc: PyMongoError):
    return JSONResponse(status_code=500, content={"detail": "MongoDB error", "error": str(exc)})

# Validation errors handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors(), "body": exc.body})

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

# MongoDB connection settings
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'weather_db'
client_mongo = MongoClient(MONGO_URI)
db_mongo = client_mongo[MONGO_DB]

# Pydantic models for MongoDB
class MongoLocation(BaseModel):
    id: str
    name: str
    state: Optional[str] = None

class MongoObservation(BaseModel):
    id: str
    location_id: str
    date: datetime
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

class MongoPrediction(BaseModel):
    id: str
    observation_id: str
    will_it_rain: bool
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

# CRUD endpoints for MongoDB Locations
@app.post("/mongo/locations/", response_model=MongoLocation)
def create_mongo_location(loc: LocationBase):
    result = db_mongo.locations.insert_one(loc.dict())
    return MongoLocation(id=str(result.inserted_id), **loc.dict())

@app.get("/mongo/locations/", response_model=List[MongoLocation])
def read_mongo_locations():
    docs = db_mongo.locations.find()
    return [MongoLocation(id=str(d["_id"]), name=d["name"], state=d.get("state")) for d in docs]

@app.get("/mongo/locations/{loc_id}", response_model=MongoLocation)
def read_mongo_location(loc_id: str):
    try:
        doc = db_mongo.locations.find_one({"_id": ObjectId(loc_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if not doc:
        raise HTTPException(status_code=404, detail="Location not found")
    return MongoLocation(id=str(doc["_id"]), name=doc["name"], state=doc.get("state"))

@app.put("/mongo/locations/{loc_id}", response_model=MongoLocation)
def update_mongo_location(loc_id: str, loc: LocationBase):
    try:
        res = db_mongo.locations.update_one({"_id": ObjectId(loc_id)}, {"$set": loc.dict()})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    doc = db_mongo.locations.find_one({"_id": ObjectId(loc_id)})
    return MongoLocation(id=str(doc["_id"]), name=doc["name"], state=doc.get("state"))

@app.delete("/mongo/locations/{loc_id}", status_code=204)
def delete_mongo_location(loc_id: str):
    try:
        res = db_mongo.locations.delete_one({"_id": ObjectId(loc_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Location not found")

# CRUD endpoints for MongoDB Observations
@app.post("/mongo/observations/", response_model=MongoObservation)
def create_mongo_observation(obs: ObservationBase):
    data = obs.dict()
    # cast date to datetime
    data["date"] = obs.date
    result = db_mongo.weather_observations.insert_one(data)
    return MongoObservation(id=str(result.inserted_id), **data)

@app.get("/mongo/observations/", response_model=List[MongoObservation])
def read_mongo_observations():
    docs = db_mongo.weather_observations.find()
    return [MongoObservation(id=str(d["_id"]), **{k: d.get(k) for k in ObservationBase.__fields__}) for d in docs]

@app.get("/mongo/observations/{obs_id}", response_model=MongoObservation)
def read_mongo_observation(obs_id: str):
    try:
        doc = db_mongo.weather_observations.find_one({"_id": ObjectId(obs_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if not doc:
        raise HTTPException(status_code=404, detail="Observation not found")
    return MongoObservation(id=str(doc["_id"]), **{k: doc.get(k) for k in ObservationBase.__fields__})

@app.put("/mongo/observations/{obs_id}", response_model=MongoObservation)
def update_mongo_observation(obs_id: str, obs: ObservationBase):
    data = obs.dict()
    try:
        res = db_mongo.weather_observations.update_one({"_id": ObjectId(obs_id)}, {"$set": data})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Observation not found")
    doc = db_mongo.weather_observations.find_one({"_id": ObjectId(obs_id)})
    return MongoObservation(id=str(doc["_id"]), **{k: doc.get(k) for k in ObservationBase.__fields__})

@app.delete("/mongo/observations/{obs_id}", status_code=204)
def delete_mongo_observation(obs_id: str):
    try:
        res = db_mongo.weather_observations.delete_one({"_id": ObjectId(obs_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Observation not found")

# CRUD endpoints for MongoDB Predictions
@app.post("/mongo/predictions/", response_model=MongoPrediction)
def create_mongo_prediction(pred: PredictionBase):
    data = pred.dict()
    data["predicted_at"] = datetime.utcnow()
    result = db_mongo.rain_predictions.insert_one(data)
    return MongoPrediction(id=str(result.inserted_id), **data)

@app.get("/mongo/predictions/", response_model=List[MongoPrediction])
def read_mongo_predictions():
    docs = db_mongo.rain_predictions.find()
    return [MongoPrediction(id=str(d["_id"]), observation_id=str(d.get("observation_id")), will_it_rain=d.get("will_it_rain"), predicted_at=d.get("predicted_at")) for d in docs]

@app.get("/mongo/predictions/{pred_id}", response_model=MongoPrediction)
def read_mongo_prediction(pred_id: str):
    try:
        doc = db_mongo.rain_predictions.find_one({"_id": ObjectId(pred_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if not doc:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return MongoPrediction(id=str(doc["_id"]), observation_id=str(doc.get("observation_id")), will_it_rain=doc.get("will_it_rain"), predicted_at=doc.get("predicted_at"))

@app.put("/mongo/predictions/{pred_id}", response_model=MongoPrediction)
def update_mongo_prediction(pred_id: str, pred: PredictionBase):
    data = pred.dict()
    try:
        res = db_mongo.rain_predictions.update_one({"_id": ObjectId(pred_id)}, {"$set": data})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Prediction not found")
    doc = db_mongo.rain_predictions.find_one({"_id": ObjectId(pred_id)})
    return MongoPrediction(id=str(doc["_id"]), observation_id=str(doc.get("observation_id")), will_it_rain=doc.get("will_it_rain"), predicted_at=doc.get("predicted_at"))

@app.delete("/mongo/predictions/{pred_id}", status_code=204)
def delete_mongo_prediction(pred_id: str):
    try:
        res = db_mongo.rain_predictions.delete_one({"_id": ObjectId(pred_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Prediction not found")
