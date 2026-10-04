'use client';

import React, { useEffect, useRef } from "react";
import { ShieldAlert, X } from "lucide-react";
import { SightingEvent } from "@/types";

interface WatchlistModalProps {
  alert: NonNullable<SightingEvent['alert']> | null;
  onDismiss: () => void;
}

export default function WatchlistModal({ alert, onDismiss }: WatchlistModalProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (alert) {
      audioRef.current = new Audio("/sounds/intercept_alarm.mp3");
      audioRef.current.play().catch(() => {
        console.warn("Audio autoplay blocked by browser policy.");
      });
    }
  }, [alert]);

  if (!alert) return null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-red-950 border-2 border-red-500 rounded-xl max-w-lg w-full p-6 shadow-[0_0_50px_rgba(239,68,68,0.4)]">
        <div className="flex justify-between items-start">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-red-600 rounded-lg text-white animate-pulse">
              <ShieldAlert className="w-8 h-8" />
            </div>
            <div>
              <span className="text-xs font-mono font-bold tracking-widest text-red-300 uppercase">
                {alert.severity} PRIORITY HIT
              </span>
              <h2 className="text-2xl font-black text-white">{alert.plate_number}</h2>
            </div>
          </div>
          <button onClick={onDismiss} className="text-slate-400 hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="mt-4 space-y-2 text-sm bg-red-900/40 p-4 rounded-lg border border-red-500/30">
          <div className="flex justify-between">
            <span className="text-red-300">Case Reference:</span>
            <span className="font-mono font-bold text-white">{alert.case_ref}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-red-300">Offense:</span>
            <span className="font-semibold text-white">{alert.crime_category}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-red-300">Trigger Camera:</span>
            <span className="font-semibold text-emerald-400">{alert.camera}</span>
          </div>
        </div>

        <div className="mt-6 flex gap-3">
          <button
            onClick={onDismiss}
            className="flex-1 py-2.5 bg-red-600 hover:bg-red-500 text-white font-bold rounded-lg text-sm transition"
          >
            Acknowledge & Dispatch PCR Van
          </button>
        </div>
      </div>
    </div>
  );
}
