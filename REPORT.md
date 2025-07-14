# Database Weather Prediction Pipeline Project Report
**Group 15**

## GitHub Repository
[Database_Prediction_Pipeline_Group15](https://github.com/Branis333/Database_Prediction_Pipeline_Group15-)

## Project Overview
Our team successfully implemented a comprehensive weather prediction pipeline that combines traditional database operations with modern machine learning techniques. The project was divided into three main tasks, each handled by different team members.

## Team Contributions

### Task 1 - Database Setup and Schema Design
**Team Member:** [Name]
[To be filled by team member responsible for Task 1]

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

### API Enhancements (Task 2):
1. Add pagination for list endpoints
2. Implement caching for frequently accessed data
3. Add more advanced filtering options
4. Implement rate limiting
5. Add authentication and authorization

### Model Enhancements (Task 3):
1. Integrate model monitoring to track accuracy drift over time
2. Allow user input for ad-hoc predictions via a frontend or API
