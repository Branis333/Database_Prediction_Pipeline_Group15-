db.locations.insertOne({
    db.weather_observations.insertOne({
        db.rain_predictions.insertOne({
            // MongoDB Collection Structure for Weather Data

            // locations collection
            db.locations.insertOne({
                name: "Sydney",
                state: "NSW"
            });

            // weather_observations collection
            db.weather_observations.insertOne({
                location_id: ObjectId("686d58b7720a08c2da2e5749"), // Reference to locations _id
                date: ISODate("2023-07-08"),
                min_temp: 10.5,
                max_temp: 18.2,
                rainfall: 2.0
            });

            // rain_predictions collection
            db.rain_predictions.insertOne({
                observation_id: ObjectId("686d58ea720a08c2da2e574a"), // Reference to weather_observations _id
                will_it_rain: true,
                predicted_at: ISODate("2023-07-08T12:00:00Z")
            });
