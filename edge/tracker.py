from collections import defaultdict
from typing import Optional, Dict

class MultiFrameVoter:
    def __init__(self, min_votes: int = 3, max_history: int = 15):
        self.min_votes = min_votes
        self.max_history = max_history
        self.history = defaultdict(list)
        self.emitted = set()

    def add_observation(self, track_id: int, plate_data: dict) -> Optional[dict]:
        if track_id in self.emitted or not plate_data.get("clean_text"):
            return None

        self.history[track_id].append(plate_data)
        if len(self.history[track_id]) > self.max_history:
            self.history[track_id].pop(0)

        valid_candidates = [obs for obs in self.history[track_id] if obs["is_valid"]]
        pool = valid_candidates if valid_candidates else self.history[track_id]

        if len(pool) >= self.min_votes:
            score_map: Dict[str, float] = defaultdict(float)
            count_map: Dict[str, int] = defaultdict(int)

            for obs in pool:
                p = obs["clean_text"]
                score_map[p] += obs["confidence"]
                count_map[p] += 1

            best_plate = max(score_map, key=lambda k: (count_map[k], score_map[k]))
            avg_conf = score_map[best_plate] / count_map[best_plate]

            self.emitted.add(track_id)
            return {
                "track_id": track_id,
                "plate_number": best_plate,
                "confidence": round(avg_conf, 3),
                "total_frames_voted": len(pool)
            }
        return None

    def purge_track(self, track_id: int):
        self.history.pop(track_id, None)
        self.emitted.discard(track_id)
