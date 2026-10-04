export interface RouteLeg {
  from_camera: string;
  to_camera: string;
  from_coords: [number, number];
  to_coords: [number, number];
  departure_time: string;
  arrival_time: string;
  speed_kmh: number;
  distance_meters: number;
  reconciled: boolean;
  reconciliation_details?: string;
  snapshot_thumbnail?: string;
}

export interface Prediction {
  predicted_junction: string;
  junction_name: string;
  coordinates: [number, number];
  probability: number;
  eta_window_minutes: string;
}

export interface TrajectoryData {
  queried_plate: string;
  canonical_plate: string;
  total_legs: number;
  legs: RouteLeg[];
  prediction: Prediction | null;
  status: string;
}

export interface SightingEvent {
  event_type: string;
  camera_id: string;
  camera_name: string;
  plate_number: string;
  raw_plate: string;
  confidence: number;
  vehicle_class: string;
  vehicle_color: string;
  timestamp: string;
  is_reconciled: boolean;
  reconciliation_reason?: string;
  thumbnail?: string;
  alert?: {
    type: string;
    plate_number: string;
    case_ref: string;
    crime_category: string;
    severity: string;
    camera: string;
  } | null;
}
