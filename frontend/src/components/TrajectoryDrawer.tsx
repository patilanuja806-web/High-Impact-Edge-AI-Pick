'use client';

import React from "react";
import { TrajectoryData } from "@/types";
import { AlertCircle, Clock, Compass, FileDown } from "lucide-react";
import { exportTrajectoryPdf } from "@/utils/exportPdf";

interface TrajectoryDrawerProps {
  trajectory: TrajectoryData | null;
  onClose: () => void;
}

export default function TrajectoryDrawer({ trajectory, onClose }: TrajectoryDrawerProps) {
  if (!trajectory) return null;

  return (
    <aside className="w-96 bg-slate-900 border-l border-slate-800 flex flex-col h-full text-slate-100 shadow-2xl z-20">
      <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-950/60">
        <div>
          <span className="text-xs font-mono text-emerald-400">VEHICLE TRACK ACTIVE</span>
          <h2 className="text-xl font-black tracking-wider text-white">{trajectory.canonical_plate}</h2>
        </div>
        <button
          onClick={() => exportTrajectoryPdf(trajectory)}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-semibold transition"
          title="Export Judicial Evidence Dossier"
        >
          <FileDown className="w-4 h-4" /> PDF
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {trajectory.prediction && (
          <div className="bg-amber-950/40 border border-amber-500/50 rounded-lg p-3 text-amber-200">
            <div className="flex items-center gap-2 mb-1">
              <Compass className="w-4 h-4 text-amber-400 animate-spin" />
              <span className="text-xs font-bold uppercase tracking-wide">Downstream Prediction</span>
            </div>
            <p className="text-sm font-semibold text-white">{trajectory.prediction.junction_name}</p>
            <div className="flex justify-between items-center text-xs mt-2 text-amber-300">
              <span>Confidence: {(trajectory.prediction.probability * 100).toFixed(0)}%</span>
              <span className="bg-amber-500/20 px-2 py-0.5 rounded border border-amber-500/30">
                ETA: {trajectory.prediction.eta_window_minutes} mins
              </span>
            </div>
          </div>
        )}

        <div className="space-y-4">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Chronological Leg Sequence</h3>
          {trajectory.legs.map((leg, index) => (
            <div key={index} className="relative pl-6 border-l-2 border-emerald-500/40 space-y-2">
              <div className="absolute -left-2 top-0 w-3.5 h-3.5 rounded-full bg-emerald-500 border-2 border-slate-900" />
              <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60">
                <div className="flex justify-between items-start">
                  <span className="text-xs font-bold text-slate-200">{leg.from_camera} ➔ {leg.to_camera}</span>
                  <span className="text-xs font-mono text-emerald-400">{leg.speed_kmh} km/h</span>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-slate-400 mt-1">
                  <Clock className="w-3 h-3" />
                  <span>{new Date(leg.arrival_time).toLocaleTimeString()}</span>
                  <span>({leg.distance_meters}m)</span>
                </div>

                {leg.snapshot_thumbnail && (
                  <div className="mt-2">
                    <img
                      src={`data:image/jpeg;base64,${leg.snapshot_thumbnail}`}
                      alt="Plate Snapshot"
                      className="w-full h-16 object-cover rounded border border-slate-700"
                    />
                  </div>
                )}

                {leg.reconciled && (
                  <div className="mt-2 bg-indigo-950/60 border border-indigo-500/40 rounded p-2 text-xs text-indigo-300">
                    <div className="flex items-center gap-1 font-bold text-indigo-200 mb-0.5">
                      <AlertCircle className="w-3.5 h-3.5 text-indigo-400" /> Reconciled Match
                    </div>
                    {leg.reconciliation_details}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 border-t border-slate-800 bg-slate-950/60">
        <button
          onClick={onClose}
          className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-xs font-bold uppercase tracking-wider transition"
        >
          Close Drawer
        </button>
      </div>
    </aside>
  );
}
