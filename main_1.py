# ---------- Imports ----------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from shapely.geometry import Polygon, Point
from datetime import datetime, timedelta
from typing import List, Dict
from geo_metrics_utils import GeoMetricsUtils
from geo_cluster_analyzer import GeoClusterAnalyzer
from geo_scoring_evaluator import GeoScoringEvaluator

# ---------- FastAPI App ----------
app = FastAPI()

# ---------- Input Schemas ----------
# ---------- Modelos de entrada ----------
class MetricasZona(BaseModel):
    velocidad_media_kmh: float
    tiempo_medio: float # en horas
    distancia_media_km: float

class ZonaFrecuente(BaseModel):
    zone_id: str
    polygon: List[List[float]]  # lista de [lon, lat]
    metricas: MetricasZona 
    
class SessionInput(BaseModel):
    user_id: str
    session_id: str
    datetime: datetime
    latitude: float
    longitude: float

class SessionOutput(BaseModel):
    from_id: int
    to_id: int
    lat_last: float
    lon_last: float
    velocity_kmh: float
    time_diff: timedelta
    distance_km: float

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
                "cluster_category": category
            })

        return {
            "status": "ok",
            "message": "GeoClusterAnalyzer is working",
            "result": categorized_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GeoClusterAnalyzer failed: {str(e)}")
    
@app.get("/health/scoring_val")
def scoring_val_health_check():
    zona = {
        "zone_id": "zona_1",
        "geometry": Polygon([
            (-58.40, -34.61),
            (-58.39, -34.61),
            (-58.39, -34.60),
            (-58.40, -34.60),
            (-58.40, -34.61)
        ]),
        "metricas": {
            "velocidad_media_kmh": 30,
            "tiempo_medio": timedelta(hours=2),
            "distancia_media_km": 5
        }
    }

    sesion = {
        "lat": -34.605,
        "lon": -58.395,
        "velocidad_kmh": 32,
        "tiempo_entre_sesiones": timedelta(hours=1.5),
        "distancia_km": 4.8
    }

    evaluator = GeoScoringEvaluator()
    result = evaluator.evaluate_session(sesion, [zona])
    return result

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

@app.post("/val/score-val")
def evaluate_session_api(SessionOutput: SessionOutput, zonas: List[ZonaFrecuente]):
    zonas_convertidas = []
    for z in zonas:
        geom = Polygon(z.polygon)
        zonas_convertidas.append({
            "zone_id": z.zone_id,
            "geometry": geom,
            "metricas": {
                "velocidad_media_kmh": z.metricas.velocidad_media_kmh,
                "tiempo_medio": timedelta(hours=z.metricas.tiempo_medio) if z.metricas.tiempo_medio else None,
                "distancia_media_km": z.metricas.distancia_media_km
            }
        })

    sesion_dict = {
        "lat": SessionOutput.lat_last,
        "lon": SessionOutput.lon_last,
        "velocity_kmh": SessionOutput.velocity_kmh,
        "time_diff": SessionOutput.time_diff,
        "distance_km": SessionOutput.distance_km
    }

    evaluator = GeoScoringEvaluator()
    return evaluator.evaluate_session(sesion_dict, zonas_convertidas)