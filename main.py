# ---------- Imports ----------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from geo_metrics_utils import GeoMetricsUtils
from geo_cluster_analyzer import GeoClusterAnalyzer

# ---------- FastAPI App ----------
app = FastAPI()

# ---------- Input Schemas ----------
class SessionInput(BaseModel):
    user_id: str
    session_id: str
    datetime: datetime
    latitude: float
    longitude: float

class SessionListInput(BaseModel):
    sessions: List[SessionInput]

class ClusterSessionInput(BaseModel):
    session_id: str
    latitude: float
    longitude: float

class ClusterSessionListInput(BaseModel):
    sessions: List[ClusterSessionInput]

# ---------- Health Endpoints ----------
@app.get("/health")
def basic_health_check():
    return {
        "status": "ok",
        "message": "API funcionando"
    }

@app.get("/health/velocity")
def velocity_health_check():
    try:
        test_sessions = [
            {"session_id": "1", "datetime": datetime(2025, 1, 1, 12, 0), "latitude": -34.6037, "longitude": -58.3816},
            {"session_id": "2", "datetime": datetime(2025, 1, 1, 14, 0), "latitude": -34.6090, "longitude": -58.3850},
            {"session_id": "3", "datetime": datetime(2025, 1, 1, 16, 30), "latitude": -34.6105, "longitude": -58.3900}
        ]
        result = GeoMetricsUtils.compare_session_list(test_sessions)

        return {
            "status": "ok",
            "message": "GeoMetricsUtils is working",
            "result": result
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GeoMetricsUtils failed: {str(e)}")

@app.get("/health/cluster")
def cluster_health_check():
    try:
        test_sessions = [
            {"session_id": "1", "latitude": -34.6037, "longitude": -58.3816},
            {"session_id": "2", "latitude": -34.6040, "longitude": -58.3820},
            {"session_id": "3", "latitude": -34.6039, "longitude": -58.3819},
            {"session_id": "4", "latitude": -34.7000, "longitude": -58.4000}
        ]

        analyzer = GeoClusterAnalyzer(eps_km=20, min_samples=3)
        raw_result = analyzer.analyze_sessions(test_sessions)

        categorized_result = []
        for r in raw_result:
            if r["cluster_id"] == -1:
                category = "ruido"
            elif r["is_main_cluster"]:
                category = "principal"
            else:
                category = "secundario"

            categorized_result.append({
                "session_id": str(r["session_id"]),
                "cluster_id": int(r["cluster_id"]),
                "is_main_cluster": bool(r["is_main_cluster"]),
                "cluster_category": category
            })

        return {
            "status": "ok",
            "message": "GeoClusterAnalyzer is working",
            "result": categorized_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GeoClusterAnalyzer failed: {str(e)}")

# ---------- Main Endpoints ----------
@app.post("/velocity/compare-last")
def compare_with_last_session(new_session: SessionInput):
    try:
        last_session = {
            "session_id": "1",
            "datetime": datetime(2025, 5, 15, 12, 30),
            "latitude": 40.0,
            "longitude": -74.0
        }

        s1 = {
            "session_id": last_session["session_id"],
            "datetime": last_session["datetime"],
            "latitude": last_session["latitude"],
            "longitude": last_session["longitude"]
        }

        s2 = {
            "session_id": new_session.session_id,
            "datetime": new_session.datetime,
            "latitude": new_session.latitude,
            "longitude": new_session.longitude
        }

        result = GeoMetricsUtils.compare_sessions(s1, s2)

        return {
            "status": "ok",
            "message": "Comparison successful",
            "result": result
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/velocity/compare-all")
def compare_all_sessions(data: SessionListInput):
    try:
        sessions_dicts = [
            {
                "session_id": s.session_id,
                "datetime": s.datetime,
                "latitude": s.latitude,
                "longitude": s.longitude
            }
            for s in data.sessions
        ]

        result = GeoMetricsUtils.compare_session_list(sessions_dicts)

        return {
            "status": "ok",
            "message": "Batch comparison successful",
            "result": result
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/geo/cluster-categorize")
def categorize_clusters(payload: ClusterSessionListInput):
    try:
        sessions_dict = [s.dict() for s in payload.sessions]

        analyzer = GeoClusterAnalyzer(eps_km=20, min_samples=3)
        raw_result = analyzer.analyze_sessions(sessions_dict)

        categorized_result = []
        for r in raw_result:
            if r["cluster_id"] == -1:
                category = "ruido"
            elif r["is_main_cluster"]:
                category = "principal"
            else:
                category = "secundario"

            categorized_result.append({
                "session_id": str(r["session_id"]),
                "cluster_id": int(r["cluster_id"]),
                "is_main_cluster": bool(r["is_main_cluster"]),
                "cluster_category": category
            })

        return {
            "status": "ok",
            "message": "Clustering successful",
            "result": categorized_result
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
