from math import radians, sin, cos, sqrt, atan2
from typing import Dict, Union
from datetime import datetime, timedelta


class GeoMetricsUtils:
    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine (en km).
        """
        R = 6371  # Radio de la Tierra en km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    @staticmethod
    def compare_sessions(session1: Dict[str, Union[str, float, datetime]],
                         session2: Dict[str, Union[str, float, datetime]]) -> Dict[str, Union[str, float, timedelta]]:
        """
        Compara dos sesiones (cada una como un diccionario con datetime, latitud y longitud).
        Espera:
            session = {
                "session_id": str,
                "datetime": datetime,
                "latitude": float,
                "longitude": float
            }
        Retorna:
            - velocity_kmh: velocidad entre sesiones en km/h
            - time_diff_hour: horas entre sesiones
            - distance_km: distancia entre sesiones en km
        """
        t1 = session1["datetime"]
        t2 = session2["datetime"]

        if not isinstance(t1, datetime) or not isinstance(t2, datetime):
            raise ValueError("Timestamps must be datetime.datetime objects")

        delta_t = t2 - t1
        hours = delta_t.total_seconds() / 3600

        distance = GeoMetricsUtils.haversine_distance_km(
            session1["latitude"], session1["longitude"],
            session2["latitude"], session2["longitude"]
        )

        velocity = distance / hours if hours > 0 else 0.0

        return {
            "user_id": int(session2["user_id"]),
            "from_id": int(session1["session_id"]),
            "to_id": int(session2["session_id"]),
            "lat_new": session2["latitude"],
            "lon_new": session2["longitude"],
            "velocity_kmh": round(velocity, 2),
            "time_diff_hour": hours,
            "distance_km": round(distance, 3)
        }