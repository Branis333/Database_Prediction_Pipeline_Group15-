# Weather Data Database & API Project

## Overview
This project demonstrates a comprehensive weather data pipeline using both PostgreSQL (Supabase) and MongoDB databases. It includes a FastAPI application for data access, data migration tools, robust data import capabilities, and machine learning-based weather prediction.

## Features

### Core Features
- Weather Data Pipeline with Dual Database System
- Machine Learning-based Rain Prediction
- RESTful API with Real-time Data Access
- Automated Data Migration Tools

### Technical Features
- Dual Database System:
  - Relational schema (PostgreSQL/Supabase)
  - NoSQL schema (MongoDB) with validation rules
- RESTful API with FastAPI
  - CRUD operations for locations, observations, and predictions
  - Support for both PostgreSQL and MongoDB operations
  - Detailed response messages and error handling
- Data Management:
  - CSV data import with chunked processing
  - Database migration tools
  - Data validation and verification
- Schema Documentation:
  - ERD diagram for PostgreSQL schema
  - MongoDB collection schemas with validation rules
  - Complete API documentation

## Project Structure
```
.
├── api/
│   ├── __init__.py
│   ├── database.py    # Database connection management
│   ├── models.py      # Pydantic models for data validation
│   └── weather_api.py # FastAPI application endpoints
├── config/
│   ├── mongodb_collections_example.js # MongoDB schema and indexes
│   └── weather_erd.dbml              # PostgreSQL ERD definition
├── data/
│   ├── weatherAUS.csv          # Weather dataset
│   ├── import_weather_data.py  # Data import script
│   ├── train_model.py         # ML model training script
│   └── rain_predictor.pkl     # Trained ML model
├── migrations/
│   ├── migrate_to_mongodb.py   # PostgreSQL to MongoDB migration
│   ├── verify_migration.py     # Migration verification tool
│   └── README.md              # Migration documentation
├── task3_prediction/
│   └── predict_latest.py      # Latest weather prediction script
├── .env            # Environment variables (create from template)
├── .gitignore      # Git ignore rules
├── requirements.txt # Python dependencies
└── README.md       # Project documentation
```

## Setup

### 1. Environment Setup
```bash
# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration
1. Copy `.env.example` to `.env` (create if needed)
2. Configure your database connections in `.env`:
   ```
   # PostgreSQL
   PG_HOST=your-host
   PG_PORT=your-port
   PG_DBNAME=your-db
   PG_USER=your-user
   PG_PASSWORD=your-password

   # MongoDB
   MONGO_URI=your-mongodb-uri
   MONGO_DB=weather_db
   ```

### 3. Database Initialization
1. Set up PostgreSQL schema:
   - Use `config/weather_erd.dbml` for reference
   - Create tables using your preferred PostgreSQL tool

2. Set up MongoDB schema:
   - Run the schema definitions from `config/mongodb_collections_example.js`

### 4. Data Import
```bash
# Import weather data into both databases
cd data
python import_weather_data.py
```

### 5. Run the API
```bash
# From the project root
uvicorn api.weather_api:app --reload
```
- Access the API documentation at http://127.0.0.1:8000/docs
- Interactive OpenAPI documentation at http://127.0.0.1:8000/redoc

## Machine Learning Model

### Model Training
```bash
# Train the weather prediction model
cd data
python train_model.py
```
The model is trained on the following features:
- Rainfall
- Maximum Temperature
- Minimum Temperature
- 9am Humidity
- 3pm Humidity

The trained model is saved as `data/rain_predictor.pkl`.

### Making Predictions
```bash
# Start the API server first
uvicorn api.weather_api:app --reload

# In a new terminal, run the prediction script
cd task3_prediction
python predict_latest.py
```

The prediction script:
1. Fetches the latest weather observation from the API
2. Preprocesses the data
3. Makes a prediction using the trained model
4. Displays the prediction result and confidence score
5. Optionally stores the prediction in both databases

## API Endpoints

### PostgreSQL Endpoints
- `/locations/` - CRUD operations for locations
- `/observations/` - CRUD operations for weather observations
- `/predictions/` - CRUD operations for rain predictions

### MongoDB Endpoints
- `/mongo/locations/` - CRUD operations for MongoDB locations
- `/mongo/observations/` - CRUD operations for MongoDB weather observations
- `/mongo/predictions/` - CRUD operations for MongoDB rain predictions

Each endpoint supports:
- GET (list & detail)
- POST (create)
- PUT (update)
- DELETE (remove)

## Database Migration

To migrate data from PostgreSQL to MongoDB:
```bash
cd migrations
python migrate_to_mongodb.py
python verify_migration.py  # Verify the migration
```

## Development Notes

### Database Design
- The API uses sequential IDs for all collections in MongoDB
- Data validation is enforced at both API and database levels
- All timestamps are stored in UTC
- Batch operations use configurable chunk sizes for performance
- Error handling includes detailed messages and proper HTTP status codes

### Machine Learning Pipeline
- RandomForest Classifier for rain prediction
- Model automatically handles missing values
- Features are preprocessed and normalized
- Predictions include probability scores
- Model performance metrics are logged

### Best Practices
- Use virtual environment for isolation
- Keep .env file secure and never commit to repository
- Run verify_migration.py after any data migration
- Monitor API performance with built-in FastAPI tools
- Regularly backup both databases

### Troubleshooting
Common issues and solutions:
1. Database Connection:
   - Verify .env configuration
   - Check database service status
   - Ensure proper network access

2. API Errors:
   - Check logs for detailed error messages
   - Verify request format matches API specs
   - Ensure all required fields are provided

3. Prediction Issues:
   - Verify model file exists (rain_predictor.pkl)
   - Check input data format
   - Ensure API is running before prediction

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and verify migrations
5. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## ERD IMAGE

![Weather ERD][imageRef]

[imageRef]: docs/Untitled.png


**Author:** Group 15
