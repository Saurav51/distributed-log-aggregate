from fastapi import APIRouter, HTTPException
from datetime import datetime

from models import LogEntry, LogResponse
from storage import LogStorage

router = APIRouter(prefix="/api/v1", tags=["logs"])
storage = LogStorage()


"""Endpoint to ingest a new log entry"""
@router.post("/logs", status_code=201)
async def ingest_log(log: LogEntry) -> dict:
    storage.add_log(
        service_name=log.service_name,
        timestamp=log.timestamp,
        message=log.message
    )
    return {"status": "success"}


"""Endpoint to query logs by service and time range"""
@router.get("/logs", response_model=list[LogResponse])
async def query_logs(
    service: str,
    start: datetime,
    end: datetime
) -> list[LogResponse]:
    if end < start:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )
    
    return storage.get_logs(service, start, end)
