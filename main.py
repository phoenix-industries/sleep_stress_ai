from fastapi import FastAPI
from routes.sleep_stress_router import router as sleep_stress_router

app = FastAPI(title="Memento AI Engine API")

app.include_router(sleep_stress_router)

@app.get("/")
def root():
    return {"status": "Memento AI Service is running."}