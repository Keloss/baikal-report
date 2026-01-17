from fastapi import FastAPI, Query
from datetime import datetime
import pytz
from app.events import get_all_events
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Baikal Report Service")

tz = pytz.timezone("Asia/Tomsk")  

@app.get("/report")
def report(
    start: str = Query(..., description="YYYY-MM-DD"),
    end: str = Query(..., description="YYYY-MM-DD"),
):
    start_dt = tz.localize(datetime.fromisoformat(start))
    end_dt = tz.localize(datetime.fromisoformat(end))

    events = get_all_events(start_dt, end_dt)
    return {"count": len(events), "events": events}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")