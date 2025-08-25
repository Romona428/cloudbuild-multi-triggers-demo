from fastapi import FastAPI
from datetime import datetime, timezone, timedelta

app = FastAPI()

@app.get("/to-datetime", summary="Convert Unix time to ISO datetime")
def to_datetime(unix_time:int, offset: int = 0):
    """
    unix_time: Unix timestamp (秒)
    offset: 時區偏移 (小時)，例如 +8 = 台灣，-5 = 紐約 (夏令時間可能不同)
    """
    tz = timezone(timedelta(hours=offset))
    dt = datetime.fromtimestamp(unix_time, tz=tz)
    return {"unix_time": unix_time, 
            "offset": f"UTC{offset:+03d}",
            "datetime": dt.isoformat()}



@app.get("/to-unix", summary="Convert ISO datetime to Unix time")
def to_unix(dt: str):
    """
    請在 Swagger UI 裡輸入例如: 2025-08-18T15:00:00+08:00
    """
    dt_obj = datetime.fromisoformat(dt)
    if dt_obj.tzinfo is None:
        dt_obj = dt_obj.replace(tzinfo=timezone.utc)
    unix_time = int(dt_obj.timestamp())
    return{"datetime": dt, "unix_time":unix_time}
    