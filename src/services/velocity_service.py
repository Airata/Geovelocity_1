from src.utils.geo_metrics_utils import GeoMetricsUtils
from datetime import datetime

def compare_with_last_session(new_session):
    # Simulamos que traemos la ultima sesion del usuario de la base de datos:
    last_session = {
        "user_id": 1,
        "session_id": 1,
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
        "user_id": new_session.user_id,
        "session_id": new_session.session_id,
        "datetime": new_session.datetime,
        "latitude": new_session.latitude,
        "longitude": new_session.longitude
    }

    return GeoMetricsUtils.compare_sessions(s1, s2)
