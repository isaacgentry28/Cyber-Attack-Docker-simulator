from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


app = FastAPI()


logs = []


class LogEntry(BaseModel):
    source: str
    message: str
    ip: Optional[str] = None
    timestamp: Optional[datetime] = None
    meta: Optional[dict] = None



@app.get("/health")
def health():
    return {"status": "ok", "time" : datetime.utcnow().isoformat()}


@app.post("/log")
def receive_log(entry: LogEntry):
    #autofill timestamp if not provided
    if not entry.timestamp:
        entry.timestamp = datetime.utcnow().isoformat()


    logs.append(entry.dict())
    print(f"[LOG] {entry.timestamp} [{entry.source}] {entry.message} ip={entry.ip} `meta={entry.meta}")
    return {"status": "stored", "total_logs": len(logs)}


@app.get("/logs")
def get_logs(limit: int = 50):
    return list(reversed(logs[- limit:]))

