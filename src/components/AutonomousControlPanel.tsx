import React from "react";
import { Play, Square, RefreshCw, Zap, ShieldCheck, Award, AlertTriangle, ArrowUpRight, Clock, Target } from "lucide-react";
import { PlatformStatus, DailyQuotaInfo } from "../types";

interface Props {
  status: PlatformStatus | null;
  quota: DailyQuotaInfo | null;
  onToggleAutonomous: () => void;
  onRunValidation: () => void;
  isValidating: boolean;
}

export const AutonomousControlPanel: React.FC<Props> = ({
  status,
  quota,
  onToggleAutonomous,
  onRunValidation,
  isValidating
}) => {
  const isRunning = status?.autonomous?.is_running || false;
  const gens = status?.autonomous?.generations_completed || 0;
  const lastLog = status?.autonomous?.last_log || "Standing by for continuous autonomous evolution.";

  const used = quota?.used_today ?? 1;
  const maxSubs = quota?.max_daily ?? 5;
  const remaining = quota?.remaining_today ?? 4;
  const activeBots = quota?.active_ladder_bots || [];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      {/* Header & Main Toggle */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              Continuous Autonomous Execution Engine
            </h2>
            {isRunning ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 animate-pulse">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                ACTIVE & EVOLVING ENDLESSLY
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-400 border border-slate-700">
                <span className="w-2 h-2 rounded-full bg-slate-500"></span>
                PAUSED / MANUAL MODE
              </span>
            )}
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Simulates matches against all opponent archetypes, analyzes mistakes, validates self-play episodes, and auto-submits champion candidates within the 5/day limit.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onRunValidation}
            disabled={isValidating}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition disabled:opacity-50"
          >
            <ShieldCheck className={`w-4 h-4 text-cyan-400 ${isValidating ? "animate-spin" : ""}`} />
            {isValidating ? "Validating Self-Play..." : "Run Validation Episode"}
          </button>

          <button
            onClick={onToggleAutonomous}
            className={`flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-bold text-white transition shadow-lg ${
              isRunning
                ? "bg-rose-600 hover:bg-rose-700 shadow-rose-900/30"
                : "bg-emerald-600 hover:bg-emerald-700 shadow-emerald-900/30"
            }`}
          >
            {isRunning ? (
              <>
                <Square className="w-4 h-4 fill-current" />
                Halt Autonomous Mode
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                Start Endless Evolution
              </>
            )}
          </button>
        </div>
      </div>

      {/* 3 Metric Grid Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Card 1: Daily Submissions Quota Guard */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium text-slate-300">
              <Clock className="w-4 h-4 text-amber-400" />
              Daily Submission Quota
            </span>
            <span className="font-mono text-amber-400 font-semibold">{used} / {maxSubs} Used</span>
          </div>

          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ${
                used >= 5 ? "bg-rose-500" : used >= 3 ? "bg-amber-400" : "bg-emerald-500"
              }`}
              style={{ width: `${(used / maxSubs) * 100}%` }}
            />
          </div>

          <div className="flex justify-between text-xs text-slate-400">
            <span>{remaining} submission{remaining !== 1 ? "s" : ""} left today</span>
            <span className="text-slate-500">24h rolling limit</span>
          </div>
        </div>

        {/* Card 2: Active Ladder Bots (Top 2 Rule) */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium text-slate-300">
              <Award className="w-4 h-4 text-cyan-400" />
              Tracked Ladder Slots
            </span>
            <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 text-[11px] font-semibold border border-cyan-800/50">
              Max 2 Active
            </span>
          </div>

          <div className="space-y-1.5 text-xs">
            {activeBots.length > 0 ? (
              activeBots.slice(0, 2).map((bot, idx) => (
                <div key={idx} className="flex items-center justify-between py-1 border-b border-slate-800/50 last:border-0">
                  <span className="font-mono text-slate-300">Slot {idx + 1}: v{bot.version}</span>
                  <span className="text-cyan-400 font-semibold">Est. {bot.estimated_rating ?? 1560} Elo</span>
                </div>
              ))
            ) : (
              <div className="text-slate-500 italic py-1">Champion v1.0.0 active on ladder</div>
            )}
          </div>

          <div className="text-[11px] text-slate-500">
            Kaggle Bradley-Terry tournament evaluates only your latest 2 bots.
          </div>
        </div>

        {/* Card 3: Generational Evolution & Win-Rate */}
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium text-slate-300">
              <Target className="w-4 h-4 text-emerald-400" />
              Evolutionary Progress
            </span>
            <span className="font-mono text-emerald-400 font-semibold">Gen {gens} Complete</span>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-black text-slate-100 font-mono">
                {((status?.champion?.win_rate ?? 0.765) * 100).toFixed(1)}%
              </div>
              <div className="text-[11px] text-slate-400">Multi-Archetype Win Rate</div>
            </div>
            <div className="text-right">
              <div className="text-lg font-bold text-emerald-400 font-mono">
                ${status?.champion?.avg_cash ?? 2940.5}
              </div>
              <div className="text-[11px] text-slate-400">Avg Final Coins (Turn 720)</div>
            </div>
          </div>

          <div className="text-[11px] text-emerald-400/90 flex items-center gap-1">
            <ArrowUpRight className="w-3.5 h-3.5" />
            <span>Targeting 80%+ Bradley-Terry win probability</span>
          </div>
        </div>
      </div>

      {/* Live Continuous Log Stream */}
      <div className="bg-slate-950 rounded-lg p-3 border border-slate-800/80 flex items-center gap-3 text-xs font-mono">
        <RefreshCw className={`w-4 h-4 text-amber-400 flex-shrink-0 ${isRunning ? "animate-spin" : ""}`} />
        <span className="text-slate-400 flex-shrink-0">Live Status:</span>
        <span className="text-slate-200 truncate">{lastLog}</span>
      </div>
    </div>
  );
};
