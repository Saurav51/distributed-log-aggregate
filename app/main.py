from fastapi import FastAPI

from routes import logs

app = FastAPI(
    title="Distributed Log Aggregator",
    description="A service for collecting and querying logs from microservices",
    version="1.0.0",
)

app.include_router(logs.router)

"""Health check endpoint"""
@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}
