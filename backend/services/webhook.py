from fastapi import APIRouter, Request, BackgroundTasks
from backend.services.hevy_sync import handle_hevy_workout

router = APIRouter()

@router.post("/webhook/hevy")
async def hevy_webhook(request: Request, background_tasks: BackgroundTasks):

    payload = await request.json()

    workout_id = payload.get("workoutId")
 
    if not workout_id:
        return {"status": "ignored"}

    # processamento em background (importante)
    background_tasks.add_task(handle_hevy_workout, workout_id)

    return {"status": "received"}