import azure.functions as func
import random
import pyodbc
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="task1")
def task1(req: func.HttpRequest) -> func.HttpResponse:
    readings = []
    for sensor_id in range(1, 21):
        reading = {
            "sensor_id": sensor_id,
            "temp": random.randint(5, 18),
            "wind": random.randint(12, 24),
            "humidity": random.randint(30, 60),
            "co2": random.randint(400, 1600)
        }
        readings.append(reading)

    try:
        connection = pyodbc.connect(os.environ["SqlConnectionString"])
        cursor = connection.cursor()

        for r in readings:
            cursor.execute(
                """
                INSERT INTO dbo.readings (sensor_id, temp, wind, humidity, co2)
                VALUES (?, ?, ?, ?, ?)
                """,
                (r["sensor_id"], r["temp"], r["wind"], r["humidity"], r["co2"])
            )

        connection.commit()
        cursor.close()
        connection.close()

        return func.HttpResponse(
            json.dumps({"message": "Data added", "data": readings}),
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(f"Database error: {e}")
