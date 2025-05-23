from typing import Dict, List, Optional, Union
from datetime import timedelta
from shapely.geometry import Point, Polygon


class GeoScoringEvaluator:
    def __init__(self, max_allowed_distance_km: float = 2.0, relative_tolerance: float = 0.3):
        """
        Clase evaluadora de sesiones basada en zonas frecuentes.
        :param max_allowed_distance_km: distancia máxima para considerar una zona como relevante.
        :param relative_tolerance: tolerancia usada para penalizar desviaciones en métricas.
        """
        self.max_dist_km = max_allowed_distance_km
        self.tolerance = relative_tolerance

    def evaluate_session(self, new_session: Dict, frequent_zones: List[Dict]) -> Dict:
        """
        Evalúa la nueva sesión comparándola con zonas frecuentes.
        :param new_session: diccionario con lat, lon, velocity_kmh, time_diff, distance_km
        :param frequent_zones: lista de zonas con "geometry" (Polygon) y "metrics" (dict)
        :return: diccionario con score, zone_val y si se encontró zone_match.
        """
        point = Point(new_session["lon"], new_session["lat"])
        best_score = 0.0
        best_zone_id = None

        for zone in frequent_zones:
            geom: Polygon = zone["geometry"]
            metrics = zone.get("metrics", {})

            if geom.contains(point):
                score_geo = 1.0
            else:
                distance_km = geom.distance(point) * 111  # grados a km
                if distance_km > self.max_dist_km:
                    continue
                score_geo = max(0.0, 1 - distance_km / self.max_dist_km)

            # Comparar métricas individuales
            score_vel = self.compare_metric(new_session.get("velocity_kmh"), metrics.get("velocity_mean_kmh"))
            score_time = self.compare_metric(new_session.get("time_diff_hour"), metrics.get("time_mean_hour"))
            score_dist = self.compare_metric(new_session.get("distance_km"), metrics.get("distance_mean_km"))

            # Score ponderado
            total_score = 0.85 * score_geo + 0.05 * score_vel + 0.05 * score_time + 0.05 * score_dist

            if total_score > best_score:
                best_score = total_score
                best_zone_id = zone["zone_id"]

        return {
            "score": best_score,
            "zone_val": best_zone_id,
            "zone_match": best_zone_id is not None
        }

    def compare_metric(self, current_value: Optional[float], average_value: Optional[float]) -> float:
        """
        Compara un valor actual contra un promedio esperado y devuelve un score entre 0 y 1.
        Penaliza desviaciones mayores que la tolerancia relativa.
        Soporta solo valores numéricos (float).
        """
        if current_value is None or average_value is None:
            return 0.5

        if average_value == 0:
            return 0.0 if current_value > 0 else 1.0

        deviation = abs(current_value - average_value) / average_value
        return max(0.0, 1 - deviation / self.tolerance)