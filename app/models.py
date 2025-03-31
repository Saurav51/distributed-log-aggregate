from datetime import datetime
from pydantic import BaseModel

"""Model for incoming log data"""
class LogEntry(BaseModel):
    service_name: str
    timestamp: datetime
    message: str

"""Model for log query responses"""
class LogResponse(BaseModel):
    timestamp: datetime
    message: str