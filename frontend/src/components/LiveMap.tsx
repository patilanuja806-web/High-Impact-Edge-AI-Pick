'use client';

import React, { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { TrajectoryData } from "@/types";

interface LiveMapProps {
  trajectory: TrajectoryData | null;
  cameras: Array<{ id: string; name: string; lat: number; lng: number }>;
}

export default function LiveMap({ trajectory, cameras }: LiveMapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapContainer.current) return;

    mapRef.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: [77.3340, 28.5645],
      zoom: 13,
    });

    mapRef.current.addControl(new maplibregl.NavigationControl(), "top-right");

    mapRef.current.on("load", () => {
      mapRef.current?.addSource("trajectory-line", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      });

      mapRef.current?.addLayer({
        id: "trajectory-path",
        type: "line",
        source: "trajectory-line",
        layout: { "line-join": "round", "line-cap": "round" },
        paint: {
          "line-color": "#EF4444",
          "line-width": 4,
          "line-dasharray": [2, 1]
        }
      });
    });

    return () => mapRef.current?.remove();
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.isStyleLoaded()) return;

    document.querySelectorAll(".camera-marker, .prediction-marker").forEach(el => el.remove());

    cameras.forEach(cam => {
      const el = document.createElement("div");
      el.className = "camera-marker w-4 h-4 bg-emerald-500 rounded-full border-2 border-slate-900 shadow-lg cursor-pointer";
      new maplibregl.Marker(el)
        .setLngLat([cam.lng, cam.lat])
        .setPopup(new maplibregl.Popup({ offset: 10 }).setHTML(`<div class="text-xs text-black font-semibold">${cam.name}</div>`))
        .addTo(map);
    });

    if (trajectory && trajectory.legs.length > 0) {
      const coordinates: [number, number][] = [];
      coordinates.push([trajectory.legs[0].from_coords[1], trajectory.legs[0].from_coords[0]]);

      trajectory.legs.forEach(leg => {
        coordinates.push([leg.to_coords[1], leg.to_coords[0]]);
      });

      const lineGeoJSON: GeoJSON.Feature<GeoJSON.LineString> = {
        type: "Feature",
        properties: {},
        geometry: {
          type: "LineString",
          coordinates: coordinates
        }
      };

      const source = map.getSource("trajectory-line") as maplibregl.GeoJSONSource;
      if (source) source.setData(lineGeoJSON);

      const bounds = coordinates.reduce((b, coord) => b.extend(coord), new maplibregl.LngLatBounds(coordinates[0], coordinates[0]));
      map.fitBounds(bounds, { padding: 60 });

      if (trajectory.prediction) {
        const pred = trajectory.prediction;
        const predEl = document.createElement("div");
        predEl.className = "prediction-marker flex items-center justify-center w-7 h-7 bg-amber-500 rounded-full animate-ping border-2 border-white";
        new maplibregl.Marker(predEl)
          .setLngLat([pred.coordinates[1], pred.coordinates[0]])
          .setPopup(new maplibregl.Popup({ offset: 15 }).setHTML(`
            <div class="text-xs text-black font-bold p-1">
              🚨 PREDICTED NEXT INTERCEPT<br/>
              ${pred.junction_name}<br/>
              Prob: ${(pred.probability * 100).toFixed(0)}% | ETA: ${pred.eta_window_minutes}m
            </div>
          `))
          .addTo(map);
      }
    }
  }, [trajectory, cameras]);

  return <div ref={mapContainer} className="w-full h-full rounded-lg shadow-inner" />;
}
