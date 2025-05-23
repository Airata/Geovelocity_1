from src.utils.geo_cluster_analyzer import GeoClusterAnalyzer

def categorize_clusters(user_id: int):
    # Simulación de consulta a la base de datos para obtener las sesiones del usuario
    sessions = [
        {"session_id": 1, "latitude": -34.6037, "longitude": -58.3816},
        {"session_id": 2, "latitude": -34.6040, "longitude": -58.3820},
        {"session_id": 3, "latitude": -34.6039, "longitude": -58.3819},
        {"session_id": 4, "latitude": -34.7000, "longitude": -58.4000}
    ]
    analyzer = GeoClusterAnalyzer(eps_km=20, min_samples=3)
    raw_result = analyzer.analyze_sessions(sessions)

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
    return categorized_result
