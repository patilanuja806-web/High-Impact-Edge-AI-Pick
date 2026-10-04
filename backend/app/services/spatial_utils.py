import math

class SpatialKinematics:
    EARTH_RADIUS_METERS = 6371000.0

    @classmethod
    def haversine_distance_meters(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return cls.EARTH_RADIUS_METERS * c

    @classmethod
    def calculate_velocity_kmh(cls, dist_meters: float, time_delta_seconds: float) -> float:
        if time_delta_seconds <= 0:
            return 0.0
        speed_mps = dist_meters / time_delta_seconds
        return speed_mps * 3.6

    @classmethod
    def is_kinematically_plausible(cls, speed_kmh: float, max_threshold_kmh: float = 140.0) -> bool:
        return 0.0 <= speed_kmh <= max_threshold_kmh
