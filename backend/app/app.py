from fastapi import FastAPI
from backend.services.webhook import router as webhook_router

app = FastAPI()

# registra o webhook
app.include_router(webhook_router)

@app.get("/")
def root():
    return {"status": "API rodando"}