# Database Weather Prediction Pipeline Project Report
**Group 15**

## GitHub Repository
[Database_Prediction_Pipeline_Group15](https://github.com/Branis333/Database_Prediction_Pipeline_Group15-)

## Project Overview
Our team successfully implemented a comprehensive weather prediction pipeline that combines traditional database operations with modern machine learning techniques. The project was divided into three main tasks, each handled by different team members.

## Team Contributions

### Task 1 - Database Setup and Schema Design

**Team Member:** Branis  
**Role:** Data Infrastructure & Database Lead

---

## Contributions

### Dual Database Architecture

- Designed a hybrid database system integrating **PostgreSQL** (via **Supabase**) for structured data and **MongoDB** for flexible document storage.
- Defined relational schema for **locations**, **observations**, and **predictions**.
- Created MongoDB collections with **schema validation** and **indexes**.

### Schema Documentation & Management

- Developed an **Entity-Relationship Diagram (ERD)** using `weather_erd.dbml` for the PostgreSQL structure.
- Provided **JSON schema definitions** in `mongodb_collections_example.js` for MongoDB collections.
- Ensured **data consistency** between both databases.

### Data Import & Migration Tools

- Created `import_weather_data.py` to load large weather datasets from CSV into both databases with **chunked processing**.
- Wrote `migrate_to_mongodb.py` and `verify_migration.py` to handle **cross-database migration** and **verification**.

### Environment Configuration

- Designed a `.env.example` template and configured **environment variables** for database connections.
- Added robust **database connection handling** in `api/database.py`.

---

## Technical Details

### PostgreSQL (Relational)

- **Tables**: Locations, WeatherObservations, RainPredictions
- **Tools**: Supabase, pgAdmin, dbml format for ERD
- **Constraints**: Primary keys, foreign keys, NOT NULL checks

### MongoDB (NoSQL)

- **Collections**: locations, observations, predictions
- **Tools**: MongoDB Compass, PyMongo
- **Features**: JSON schema validation, custom indexes for performance

---

## Scripts and Config Files

- `import_weather_data.py`: Efficient CSV import into both databases
- `mongodb_collections_example.js`: MongoDB schema and index setup
- `verify_migration.py`: Compares PostgreSQL and MongoDB data for consistency

---

## Key Achievements

- Successfully set up a **dual-database architecture**
- Automated **import and migration processes**
- Ensured **schema validation** and **data consistency** across systems
- Created robust **database initialization and verification tools**

### Task 2 - FastAPI CRUD Implementation
**Team Member:** Abiodun
**Role:** API Development Lead

#### Contributions:
1. **API Architecture Design**
   - Designed and implemented a RESTful API using FastAPI
   - Set up proper project structure following best practices
   - Implemented robust error handling and validation

2. **CRUD Endpoints Implementation**
   - Created comprehensive CRUD operations for:
     - Locations
     - Weather Observations
     - Rain Predictions
   
3. **Code Quality & Documentation**
   - Wrote detailed API documentation using FastAPI's automatic docs
   - Implemented proper type hints and Pydantic models
   - Added comprehensive error messages and status codes

#### Technical Details:

**Create (POST) Endpoints:**
```python
@app.post("/locations/")
@app.post("/observations/")
@app.post("/predictions/")
```
- Implemented input validation
- Added proper error handling
- Returns created resource with ID

**Read (GET) Endpoints:**
```python
@app.get("/locations/")
@app.get("/locations/{location_id}")
@app.get("/observations/")
@app.get("/predictions/")
```
- Supports both list and detail views
- Implements efficient database queries
- Proper response formatting

**Update (PUT) Endpoints:**
```python
@app.put("/locations/{location_id}")
@app.put("/observations/{observation_id}")
@app.put("/predictions/{prediction_id}")
```
- Validates update data
- Handles missing resources
- Returns updated resource

**Delete (DELETE) Endpoints:**
```python
@app.delete("/locations/{location_id}")
@app.delete("/observations/{observation_id}")
@app.delete("/predictions/{prediction_id}")
```
- Proper resource cleanup
- Appropriate status codes
- Error handling for non-existent resources

#### Key Achievements:
- Successfully integrated with PostgreSQL database
- Implemented proper connection pooling
- Added comprehensive input validation
- Created detailed API documentation
- Achieved 100% CRUD functionality coverage

### Task 3 - Machine Learning Integration
**Team Member:** Nicolas Muhigi
**Role:** Create a Script to Fetch Data for Prediction
#### Contributions
1. **Model Training & Saving**
   - Trained a Random Forest Classifier using relevant weather features
   - Preprocessed the dataset to handle missing values and encoded the target 
   - Split data into training and testing sets 
   - Saved trained model using joblib for future inference

2. **Prediction Script Development**
- Developed a Python script predict_latest.py to:
  - Fetch the most recent observation data from FastAPI MongoDB endpoint
  - Preprocess the data into a structured format for ML model
  - Load the trained model and perform inference
  - Print the predicted class (rain or not) and probability
 
3. **Integration with FastAPI**
   - Integrated the script with the FastAPI server to fetch live data
   - Aligned the model's expected input features with API schema fields
   - Added fallback logic for missing or incomplete API response

### Technical Details
**Model Training (train_model.py):**
- Algorithm: RandomForestClassifier from scikit-learn
- Features: ["Rainfall", "MaxTemp", "MinTemp", "Humidity9am", "Humidity3pm"]
- Target: Encoded "RainTomorrow" column
- Preprocessing:
  - Dropped rows with missing critical values
  - Used LabelEncoder for binary label encoding
- Output: rain_predictor.pkl saved in /data directory
  
**Prediction Script (predict_latest.py):**
- API Call: ```GET http://127.0.0.1:8000/mongo/observations/ ```
- Model Inference: ```model.predict(input_df)```, ```model.predict_proba(input_df)```
- Output: ```🌧️ Will it rain tomorrow? Yes/No```, ```💧 Probability of rain: XX.XX%```

### Key Achievements
- Seamlessly automated the ML prediction process from API to inference
- Enabled real-time decision making using live data
- Maintained feature consistency between training and prediction pipelines
- Created a reusable script that can be extended to store predictions or trigger alerts

## Challenges and Solutions

### Task 1 Specific Challenges:

#### Dual Database Synchronization  
**Challenge**: Keeping PostgreSQL and MongoDB in sync during imports and migrations  
**Solution**: Created migration and verification scripts (`migrate_to_mongodb.py`, `verify_migration.py`) to compare and validate consistency across both databases after each import  

#### Schema Consistency  
**Challenge**: Ensuring consistent schema across SQL (strict) and NoSQL (flexible) environments  
**Solution**: Applied JSON schema validation for MongoDB collections and enforced constraints like `NOT NULL` and foreign keys in PostgreSQL  

#### Large Dataset Import  
**Challenge**: Importing and processing large CSV files without exhausting memory  
**Solution**: Implemented chunked processing in `import_weather_data.py` to handle data in manageable batches  

#### Environment & Credential Management  
**Challenge**: Managing secure and environment-specific configurations across local/dev/prod  
**Solution**: Created `.env.example` and used environment variables in all config files for secure and consistent setup  

#### Database Connection Reliability  
**Challenge**: Handling intermittent or failed connections to either database  
**Solution**: Added robust error handling and connection retries in `api/database.py`, ensuring reliability in production  


### Task 2 Specific Challenges:
1. **Database Connection Management**
   - **Challenge:** Maintaining efficient database connections for multiple requests
   - **Solution:** Implemented connection pooling and proper connection cleanup

2. **Input Validation**
   - **Challenge:** Ensuring data consistency across endpoints
   - **Solution:** Used Pydantic models for robust validation

3. **Error Handling**
   - **Challenge:** Providing meaningful error messages
   - **Solution:** Implemented custom exception handlers and proper HTTP status codes
  
### Task 3 Specific Challenges:
1. **API Data Reliability:**
   - **Challenge:** API could return ```null``` or incomplete fields
   - **Solution:** Solution: Implemented fallback defaults ```(0)``` to ensure prediction does not break

2. **Model Input Format**
   - **Challenge:** Ensuring input format matches the model’s training structure
   - **Solution:** Used consistent feature order and names in both training and inference scripts

3. **Model Path Portability**
   - **Challenge:** File path inconsistency across environments
   - **Solution:** Used ```os.path.join``` to ensure path compatibility

## Lessons Learned

### From Task 1:
1. Dual-database systems require strong planning for synchronization and consistency
2. JSON schema validation in MongoDB is essential for maintaining data integrity  
3. Automating import and migration reduces human error and improves scalability  

### From Task 2:
1. The importance of proper API documentation
2. The value of type hints in Python
3. The benefits of using modern frameworks like FastAPI
4. The significance of proper error handling in APIs

## From Task 3:
1. Importance of aligning model training features with API data structures
2. Real-world data often contains inconsistencies that must be handled programmatically
3. ML models are only as useful as the reliability of the pipeline that surrounds them
4. Automating predictions builds a foundation for decision intelligence in web apps



## Future Improvements

### Database Enhancements (Task 1):
1. Implement real-time syncing service between PostgreSQL and MongoDB
2. Add backup scripts for both databases to support disaster recovery  
3. Optimize indexing in MongoDB and PostgreSQL for complex queries and forecasting  

### API Enhancements (Task 2):
1. Add pagination for list endpoints
2. Implement caching for frequently accessed data
3. Add more advanced filtering options
4. Implement rate limiting
5. Add authentication and authorization

### Model Enhancements (Task 3):
1. Integrate model monitoring to track accuracy drift over time
2. Allow user input for ad-hoc predictions via a frontend or API
