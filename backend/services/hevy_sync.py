import requests
import os
from ingestion import get_connection
from dotenv import load_dotenv


load_dotenv()
HEVY_API_KEY = os.getenv("HEVY_API_KEY")

def fetch_workout_details(workout_id: str):
    url = f"https://api.hevyapp.com/workouts/{workout_id}"

    headers = {
        "api-key": HEVY_API_KEY
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def delete_workout(workout_id: str):
    print(f"Deleting workout {workout_id}")


def insert_workout(workout):
    conn = get_connection()
    cursor = conn.cursor()

    for exercise in workout["exercises"]:
        exercise_title = exercise["title"]

        for i, s in enumerate(exercise["sets"]):

            cursor.execute("""
                INSERT INTO workouts (
                    title,
                    start_time,
                    end_time,
                    description,
                    exercise_title,
                    set_index,
                    set_type,
                    weight_kg,
                    reps,
                    distance_km,
                    duration_seconds,
                    rpe,
                    exercise_notes,
                    workout_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                workout.get("title"),
                workout.get("start_time"),
                workout.get("end_time"),
                workout.get("description"),
                exercise_title,
                i,
                s.get("type"),
                s.get("weight_kg"),
                s.get("reps"),
                s.get("distance_km"),
                s.get("duration_seconds"),
                s.get("rpe"),
                exercise.get("notes"),
                workout.get("id")   # 🔥 IMPORTANTE
            ))

    conn.commit()
    conn.close()



def handle_hevy_workout(workout_id: str):
    try:
        workout_data = fetch_workout_details(workout_id)

        delete_workout(workout_id)
        insert_workout(workout_data)

    except Exception as e:
        print(f"Erro ao processar workout {workout_id}: {e}")
