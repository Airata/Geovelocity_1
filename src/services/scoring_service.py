from shapely.geometry import Polygon
from src.utils.geo_scoring_evaluator import GeoScoringEvaluator

def evaluate_session(session_output, zones):
    zones_transform = []
    for z in zones:
        geom = Polygon(z.polygon)
        zones_transform.append({
            "zone_id": z.zone_id,
            "geometry": geom,
            "metrics": {
                "velocity_mean_kmh": z.metrics.velocity_mean_kmh,
                "time_mean_hour": z.metrics.time_mean_hour,
                "distance_mean_km": z.metrics.distance_mean_km
            }
        })

    sesion_dict = {
        "lat": session_output.lat_new,
        "lon": session_output.lon_new,
        "velocity_kmh": session_output.velocity_kmh,
        "time_diff_hour": session_output.time_diff_hour,
        "distance_km": session_output.distance_km
    }

    evaluator = GeoScoringEvaluator()
    return evaluator.evaluate_session(sesion_dict, zones_transform)
