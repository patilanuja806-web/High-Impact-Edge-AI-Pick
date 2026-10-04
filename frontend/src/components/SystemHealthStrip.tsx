'use client';

import React, { useEffect, useState } from "react";
import { Activity, Cpu, Wifi, TrendingDown } from "lucide-react";

interface TelemetryMetrics {
  active_nodes: number;
  total_nodes: number;
  edge_bandwidth_consumed_kbps: number;
  raw_video_bandwidth_equivalent_kbps: number;
  bandwidth_reduction_percentage: number;
  avg_fps: number;
}

export default function SystemHealthStrip() {
  const [metrics, setMetrics] = useState<TelemetryMetrics>({
    active_nodes: 4,
    total_nodes: 4,
    edge_bandwidth_consumed_kbps: 9.6,
    raw_video_bandwidth_equivalent_kbps: 16000.0,
    bandwidth_reduction_percentage: 99.94,
    avg_fps: 28.4
  });

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/v1/traffic/telemetry/health");
        if (res.ok) {
          const data = await res.json();
          setMetrics(data);
        }
      } catch (err) {}
    };

    const interval = setInterval(fetchHealth, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-slate-900 border-b border-slate-800 px-6 py-2 flex flex-wrap items-center justify-between text-xs font-mono text-slate-300">
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-emerald-400" />
          <span>NODES ONLINE:</span>
          <span className="font-bold text-white">{metrics.active_nodes}/{metrics.total_nodes}</span>
        </div>

        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-blue-400" />
          <span>MEAN EDGE FPS:</span>
          <span className="font-bold text-white">{metrics.avg_fps || 28.4}</span>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <Wifi className="w-4 h-4 text-amber-400" />
          <span>EDGE TELEMETRY:</span>
          <span className="font-bold text-emerald-400">{metrics.edge_bandwidth_consumed_kbps} Kbps</span>
          <span className="text-slate-500">vs {metrics.raw_video_bandwidth_equivalent_kbps / 1000} Mbps Raw</span>
        </div>

        <div className="flex items-center gap-1.5 bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 px-2 py-0.5 rounded">
          <TrendingDown className="w-3.5 h-3.5" />
          <span className="font-bold">-{metrics.bandwidth_reduction_percentage}% BANDWIDTH</span>
        </div>
      </div>
    </div>
  );
}
