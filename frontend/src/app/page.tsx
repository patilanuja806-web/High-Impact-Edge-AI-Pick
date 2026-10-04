'use client';

import React, { useState, useEffect } from "react";
import LiveMap from "@/components/LiveMap";
import TrajectoryDrawer from "@/components/TrajectoryDrawer";
import WatchlistModal from "@/components/WatchlistModal";
import { TrajectoryData, SightingEvent } from "@/types";
import { Search, Radio, Car } from "lucide-react";

export default function CommandConsole() {
  const [searchPlate, setSearchPlate] = useState("DL01AB1234");
  const [trajectory, setTrajectory] = useState<TrajectoryData | null>(null);
  const [feed, setFeed] = useState<SightingEvent[]>([]);
  const [activeAlert, setActiveAlert] = useState<NonNullable<SightingEvent['alert']> | null>(null);

  const cameras = [
    { id: "CAM_JNC_A", name: "Sector 18 Crossing", lat: 28.5701, lng: 77.3218 },
    { id: "CAM_JNC_B", name: "Golf Course Road", lat: 28.5645, lng: 77.3340 },
    { id: "CAM_JNC_C", name: "Metro Interchange Toll", lat: 28.5580, lng: 77.3485 },
    { id: "CAM_JNC_D", name: "Expressway North Exit", lat: 28.5490, lng: 77.3620 }
  ];

  useEffect(() => {
    let ws: WebSocket;
    try {
      ws = new WebSocket("ws://localhost:8000/ws/live");
      ws.onmessage = (event) => {
        const data: SightingEvent = JSON.parse(event.data);
        setFeed((prev) => [data, ...prev.slice(0, 19)]);
        if (data.alert) {
          setActiveAlert(data.alert);
        }
      };
    } catch (e) {
      console.warn("WebSocket not connected yet.");
    }
    return () => ws && ws.close();
  }, []);

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!searchPlate.trim()) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/trajectory/track/${searchPlate.trim()}`);
      const data = await res.json();
      setTrajectory(data);
    } catch (err) {
      console.error("Failed to retrieve trajectory:", err);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 flex-col overflow-hidden">
      <header className="h-14 border-b border-slate-800 bg-slate-900/90 px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded text-emerald-400">
            <Radio className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h1 className="text-sm font-black tracking-wider text-white">NETRAGATI COMMAND CENTER</h1>
            <p className="text-[10px] text-slate-400">CITY ANPR & SPATIAL INTERCEPT PLATFORM</p>
          </div>
        </div>

        <form onSubmit={handleSearch} className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={searchPlate}
              onChange={(e) => setSearchPlate(e.target.value.toUpperCase())}
              placeholder="SEARCH SUSPECT PLATE..."
              className="bg-slate-950 border border-slate-700 pl-9 pr-4 py-1.5 rounded text-xs font-mono font-bold tracking-widest text-emerald-400 focus:outline-none focus:border-emerald-500 w-64"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-bold transition"
          >
            TRACE
          </button>
        </form>
      </header>

      <div className="flex flex-1 relative overflow-hidden">
        <div className="w-80 border-r border-slate-800 bg-slate-900/60 p-4 flex flex-col h-full">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
            <Car className="w-4 h-4 text-emerald-400" /> Live Optical Feed
          </h2>
          <div className="flex-1 overflow-y-auto space-y-2.5">
            {feed.map((s, idx) => (
              <div
                key={idx}
                onClick={() => { setSearchPlate(s.plate_number); handleSearch(); }}
                className="bg-slate-800/60 hover:bg-slate-800 p-2.5 rounded border border-slate-700/60 cursor-pointer transition text-xs"
              >
                <div className="flex justify-between items-center">
                  <span className="font-mono font-bold text-emerald-300">{s.plate_number}</span>
                  <span className="text-[10px] text-slate-400">{new Date(s.timestamp).toLocaleTimeString()}</span>
                </div>
                <div className="text-[11px] text-slate-300 mt-1">{s.camera_name}</div>
                {s.is_reconciled && (
                  <span className="inline-block mt-1 text-[9px] bg-indigo-900/60 text-indigo-300 px-1.5 py-0.5 rounded">
                    Reconciled
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="flex-1 relative">
          <LiveMap trajectory={trajectory} cameras={cameras} />
        </div>

        <TrajectoryDrawer trajectory={trajectory} onClose={() => setTrajectory(null)} />
      </div>

      <WatchlistModal alert={activeAlert} onDismiss={() => setActiveAlert(null)} />
    </div>
  );
}
