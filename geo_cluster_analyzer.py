from sklearn.cluster import DBSCAN
import numpy as np
from typing import List, Dict, Union
from collections import Counter


class GeoClusterAnalyzer:
    def __init__(self, eps_km: float = 20, min_samples: int = 3):
        """
        eps_km: distancia máxima en kilómetros para considerar puntos vecinos
        min_samples: cantidad mínima de puntos para formar un cluster
        """
        self.eps_rad = eps_km / 6371  # Conversión a radianes
        self.min_samples = min_samples

    def analyze_sessions(self, sessions: List[Dict[str, Union[str, float]]]) -> List[Dict[str, Union[str, int, bool]]]:
        """
        Aplica DBSCAN sobre una lista de sesiones para agrupar geográficamente.

        Parámetros:
            sessions: lista de dicts con 'session_id', 'latitude', 'longitude'

        Retorna:
            Lista de dicts con:
                - session_id: str
                - cluster_id: int
                - is_main_cluster: bool
        """
        if len(sessions) < self.min_samples:
            raise ValueError("Not enough sessions to perform clustering.")

        # Extraer coordenadas geográficas
        coords = [[s["latitude"], s["longitude"]] for s in sessions]
        coords_rad = np.radians(coords)

        # Ejecutar DBSCAN con distancia haversine
        clustering = DBSCAN(
            eps=self.eps_rad,
            min_samples=self.min_samples,
            metric="haversine"
        ).fit(coords_rad)

        labels = clustering.labels_

        # Identificar el cluster más frecuente (excluyendo outliers -1)
        cluster_counts = Counter(label for label in labels if label != -1)
        main_cluster = cluster_counts.most_common(1)[0][0] if cluster_counts else None

        # Construir resultado final
        result = []
        for i, s in enumerate(sessions):
            cluster_id = int(labels[i])
            result.append({
                "session_id": str(s["session_id"]),
                "cluster_id": cluster_id,
                "is_main_cluster": bool(cluster_id == main_cluster)
            })

        return result
