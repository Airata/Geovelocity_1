from math import radians, sin, cos, sqrt, atan2
from typing import Dict, List, Union
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
            - time_diff: objeto timedelta
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
            "from_id": str(session1["session_id"]),
            "to_id": str(session2["session_id"]),
            "velocity_kmh": round(velocity, 2),
            "time_diff": delta_t,
            "distance_km": round(distance, 3)
        }

    @staticmethod
    def compare_session_list(sessions: List[Dict[str, Union[str, float, datetime]]]) -> List[Dict[str, Union[str, float, timedelta]]]:
        """
        Compara una lista de sesiones consecutivas y devuelve métricas entre pares.
        Cada sesión debe tener: session_id, datetime, latitude, longitude.
        """
        if len(sessions) < 2:
            raise ValueError("At least two sessions are required for comparison.")

        # Ordenar por datetime por seguridad
        sessions_sorted = sorted(sessions, key=lambda s: s["datetime"])
        results = []

        for i in range(len(sessions_sorted) - 1):
            s1 = sessions_sorted[i]
            s2 = sessions_sorted[i + 1]
            metrics = GeoMetricsUtils.compare_sessions(s1, s2)
            results.append(metrics)

        return results
