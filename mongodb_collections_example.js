// Create indexes for MongoDB collections

// Create unique indexes for primary key simulation
db.locations.createIndex({ "_id": 1 }, { unique: true });
db.weather_observations.createIndex({ "_id": 1 }, { unique: true });
db.rain_predictions.createIndex({ "_id": 1 }, { unique: true });

// Create indexes for foreign key relationships
db.weather_observations.createIndex({ "location_id": 1 });  // References locations
db.rain_predictions.createIndex({ "observation_id": 1 });   // References weather_observations

// Create compound indexes for common query patterns
db.weather_observations.createIndex({ "location_id": 1, "date": 1 });  // For querying observations by location and date
db.weather_observations.createIndex({ "date": 1 });  // For date-based queries
db.rain_predictions.createIndex({ "predicted_at": 1 });  // For timestamp-based queries

// Example documents for each collection
// MongoDB Collection Structure for Weather Data

            // locations collection
            db.locations.insertOne({
                name: "Sydney",
                state: "NSW"
            });

            // weather_observations collection with all fields matching PostgreSQL
            db.weather_observations.insertOne({
                location_id: ObjectId("686d58b7720a08c2da2e5749"), // Reference to locations _id
                date: ISODate("2023-07-08"),
                min_temp: 10.5,
                max_temp: 18.2,
                rainfall: 2.0,
                humidity_9am: 71.0,
                humidity_3pm: 43.0,
                pressure_9am: 1010.5,
                pressure_3pm: 1009.2,
                wind_speed_9am: 15.0,
                wind_speed_3pm: 20.0,
                wind_dir_9am: "SE",
                wind_dir_3pm: "SSE",
                cloud_9am: 4,
                cloud_3pm: 6,
                temp_9am: 15.5,
                temp_3pm: 21.3,
                rain_today: false,
                rain_tomorrow: false
            });

            // rain_predictions collection
            db.rain_predictions.insertOne({
                observation_id: ObjectId("686d58ea720a08c2da2e574a"), // Reference to weather_observations _id
                will_it_rain: true,
                predicted_at: ISODate("2023-07-08T12:00:00Z")
            });
