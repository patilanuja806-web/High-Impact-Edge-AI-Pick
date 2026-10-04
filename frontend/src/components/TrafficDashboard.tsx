'use client';

import React, { useState } from "react";
import { ArrowRight, AlertTriangle, Gauge, Car } from "lucide-react";

interface ODItem {
  origin_name: string;
  destination_name: string;
  volume: number;
  average_speed_kmh: number;
  transit_duration_minutes: number;
}

interface CongestionNode {
  junction_name: string;
  density_per_minute: number;
  congestion_level: 'GREEN' | 'ORANGE' | 'RED';
  early_bottleneck_warning: boolean;
}

export default function TrafficDashboard() {
  const [odMatrix] = useState<ODItem[]>([
    { origin_name: "Sector 18 Crossing", destination_name: "Golf Course Road", volume: 142, average_speed_kmh: 38.4, transit_duration_minutes: 2.2 },
    { origin_name: "Golf Course Road", destination_name: "Metro Interchange Toll", volume: 98, average_speed_kmh: 44.1, transit_duration_minutes: 2.3 },
    { origin_name: "Metro Interchange Toll", destination_name: "Expressway North Exit", volume: 85, average_speed_kmh: 52.0, transit_duration_minutes: 2.1 }
  ]);

  const [congestionList] = useState<CongestionNode[]>([
    { junction_name: "Sector 18 Crossing", density_per_minute: 7.8, congestion_level: "ORANGE", early_bottleneck_warning: true },
    { junction_name: "Golf Course Road", density_per_minute: 4.2, congestion_level: "GREEN", early_bottleneck_warning: false },
    { junction_name: "Metro Interchange Toll", density_per_minute: 9.4, congestion_level: "RED", early_bottleneck_warning: true },
    { junction_name: "Expressway North Exit", density_per_minute: 3.1, congestion_level: "GREEN", early_bottleneck_warning: false }
  ]);

  return (
    <div className="p-6 space-y-6 bg-slate-950 text-slate-100 h-full overflow-y-auto">
      <div className="space-y-2">
        {congestionList.filter(c => c.early_bottleneck_warning).map((c, i) => (
          <div key={i} className="flex items-center gap-3 bg-amber-950/40 border border-amber-500/60 p-3 rounded-lg text-amber-200">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
            <div className="text-xs">
              <span className="font-bold">EARLY BOTTLENECK ALERT: </span>
              Inflow at <span className="font-semibold text-white">{c.junction_name}</span> exceeds normal threshold (+50% rate spike, {c.density_per_minute} veh/min). Signal phase adjustment recommended.
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="flex items-center gap-2 mb-4">
            <Car className="w-5 h-5 text-emerald-400" />
            <h3 className="font-bold text-sm tracking-wider uppercase text-white">Origin-Destination (OD) Corridor Volume</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="border-b border-slate-800 text-slate-400">
                <tr>
                  <th className="pb-2">CORRIDOR SEGMENT</th>
                  <th className="pb-2 text-right">VOLUME</th>
                  <th className="pb-2 text-right">AVG SPEED</th>
                  <th className="pb-2 text-right">TRANSIT TIME</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {odMatrix.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition">
                    <td className="py-2.5 flex items-center gap-1.5">
                      <span>{row.origin_name}</span>
                      <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
                      <span>{row.destination_name}</span>
                    </td>
                    <td className="py-2.5 text-right font-bold text-white">{row.volume}</td>
                    <td className="py-2.5 text-right text-emerald-400">{row.average_speed_kmh} km/h</td>
                    <td className="py-2.5 text-right text-blue-400">{row.transit_duration_minutes}m</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="flex items-center gap-2 mb-4">
            <Gauge className="w-5 h-5 text-blue-400" />
            <h3 className="font-bold text-sm tracking-wider uppercase text-white">Junction Congestion Status</h3>
          </div>
          <div className="space-y-3">
            {congestionList.map((jnc, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-700/50 text-xs">
                <div>
                  <div className="font-semibold text-white">{jnc.junction_name}</div>
                  <div className="text-[11px] text-slate-400 font-mono mt-0.5">
                    Flow: {jnc.density_per_minute} vehicles / minute
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-2.5 py-1 rounded font-bold text-[10px] tracking-wider uppercase ${
                    jnc.congestion_level === "RED"
                      ? "bg-red-950 text-red-400 border border-red-500/50"
                      : jnc.congestion_level === "ORANGE"
                      ? "bg-amber-950 text-amber-400 border border-amber-500/50"
                      : "bg-emerald-950 text-emerald-400 border border-emerald-500/50"
                  }`}>
                    {jnc.congestion_level}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
