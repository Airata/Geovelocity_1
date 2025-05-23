from pydantic import BaseModel
from datetime import datetime
from typing import List

class MetricsZone(BaseModel):
    velocity_mean_kmh: float
    time_mean_hour: float
    distance_mean_km: float

class FrecuentsZone(BaseModel):
    zone_id: int
    polygon: List[List[float]]
    metrics: MetricsZone

class SessionInput(BaseModel):
    user_id: int
    session_id: int
    datetime: datetime
    latitude: float
    longitude: float

class SessionOutput(BaseModel):
    from_id: int
    to_id: int
    lat_new: float
    lon_new: float
    velocity_kmh: float
    time_diff_hour: float
    distance_km: float

class ScoreRequest(BaseModel):
    session: SessionOutput
    zones: List[FrecuentsZone]