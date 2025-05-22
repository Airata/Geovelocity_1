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
        :param new_session: diccionario con lat, lon, velocidad_kmh, tiempo_entre_sesiones_horas, distancia_km
        :param frequent_zones: lista de zonas con "geometry" (Polygon) y "metricas" (dict)
        :return: diccionario con score_final, zona_evaluada y si se encontró una zona candidata.
        """
        point = Point(new_session["lon"], new_session["lat"])
        best_score = 0.0
        best_zone_id = None

        for zone in frequent_zones:
            geom: Polygon = zone["geometry"]
            metrics = zone.get("metricas", {})

            if geom.contains(point):
                score_geo = 1.0
            else:
                distance_km = geom.distance(point) * 111  # grados a km
                if distance_km > self.max_dist_km:
                    continue
                score_geo = max(0.0, 1 - distance_km / self.max_dist_km)

            # Comparar métricas individuales
            score_vel = self.compare_metric(new_session.get("velocidad_kmh"), metrics.get("velocidad_media_kmh"))
            score_time = self.compare_metric(new_session.get("tiempo_entre_sesiones"), metrics.get("tiempo_medio"))
            score_dist = self.compare_metric(new_session.get("distancia_km"), metrics.get("distancia_media_km"))

            # Score ponderado
            total_score = 0.7 * score_geo + 0.1 * score_vel + 0.1 * score_time + 0.1 * score_dist

            if total_score > best_score:
                best_score = total_score
                best_zone_id = zone["zone_id"]

        return {
            "score": best_score,
            "zone_val": best_zone_id,
            "zone_match": best_zone_id is not None
        }

    def compare_metric(self, current_value: Optional[Union[float, timedelta]], 
                            average_value: Optional[Union[float, timedelta]]) -> float:
        """
        Compara un valor actual contra un promedio esperado y devuelve un score entre 0 y 1.
        Penaliza desviaciones mayores que la tolerancia relativa.
        Soporta valores numéricos y objetos timedelta.
        """
        if current_value is None or average_value is None:
            return 0.5

        # Si son timedelta, convertir a horas
        if isinstance(current_value, timedelta) and isinstance(average_value, timedelta):
            current_value = current_value.total_seconds() / 3600
            average_value = average_value.total_seconds() / 3600

        if average_value == 0:
            return 0.0 if current_value > 0 else 1.0

        deviation = abs(current_value - average_value) / average_value
        return max(0.0, 1 - deviation / self.tolerance)