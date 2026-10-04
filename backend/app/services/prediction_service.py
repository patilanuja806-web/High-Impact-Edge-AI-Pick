import networkx as nx
from typing import Optional
from backend.app.schemas.trajectory import NextJunctionPrediction

class CorridorPredictor:
    def __init__(self):
        self.road_graph = nx.DiGraph()
        self._init_topology()

    def _init_topology(self):
        self.road_graph.add_node("CAM_JNC_A", name="Sector 18 Crossing", lat=28.5701, lng=77.3218)
        self.road_graph.add_node("CAM_JNC_B", name="Golf Course Road", lat=28.5645, lng=77.3340)
        self.road_graph.add_node("CAM_JNC_C", name="Metro Interchange Toll", lat=28.5580, lng=77.3485)
        self.road_graph.add_node("CAM_JNC_D", name="Expressway North Exit", lat=28.5490, lng=77.3620)

        self.road_graph.add_edge("CAM_JNC_A", "CAM_JNC_B", distance=1400, default_speed=40.0, transition_prob=0.85)
        self.road_graph.add_edge("CAM_JNC_B", "CAM_JNC_C", distance=1700, default_speed=45.0, transition_prob=0.88)
        self.road_graph.add_edge("CAM_JNC_C", "CAM_JNC_D", distance=1800, default_speed=55.0, transition_prob=0.84)
        
        self.road_graph.add_edge("CAM_JNC_D", "CAM_JNC_C", distance=1800, default_speed=55.0, transition_prob=0.80)
        self.road_graph.add_edge("CAM_JNC_C", "CAM_JNC_B", distance=1700, default_speed=45.0, transition_prob=0.82)
        self.road_graph.add_edge("CAM_JNC_B", "CAM_JNC_A", distance=1400, default_speed=40.0, transition_prob=0.80)

    def predict_next(self, current_camera_id: str, prev_camera_id: Optional[str] = None) -> Optional[NextJunctionPrediction]:
        if current_camera_id not in self.road_graph:
            return None

        successors = list(self.road_graph.successors(current_camera_id))
        if not successors:
            return None

        viable_targets = [s for s in successors if s != prev_camera_id] if prev_camera_id and len(successors) > 1 else successors
        if not viable_targets:
            viable_targets = successors

        best_target = max(viable_targets, key=lambda target: self.road_graph[current_camera_id][target].get("transition_prob", 0.5))
        edge_data = self.road_graph[current_camera_id][best_target]
        target_node = self.road_graph.nodes[best_target]

        distance_km = edge_data["distance"] / 1000.0
        speed_kmh = edge_data["default_speed"]
        eta_minutes_exact = (distance_km / speed_kmh) * 60.0
        
        min_eta = max(1, int(round(eta_minutes_exact * 0.8)))
        max_eta = int(round(eta_minutes_exact * 1.3))

        return NextJunctionPrediction(
            predicted_junction=best_target,
            junction_name=target_node["name"],
            coordinates=[target_node["lat"], target_node["lng"]],
            probability=edge_data["transition_prob"],
            eta_window_minutes=f"{min_eta}-{max_eta}"
        )
