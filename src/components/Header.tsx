import React from "react";
import { Cpu, Trophy, Bot, Sparkles, RefreshCw, Send, Play } from "lucide-react";
import { PlatformStatus } from "../types";

interface HeaderProps {
  status: PlatformStatus | null;
  onRunSimulation: () => void;
  onOptimize: () => void;
  onSubmitKaggle: () => void;
  isSimulating: boolean;
  isOptimizing: boolean;
  isSubmitting: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  status,
  onRunSimulation,
  onOptimize,
  onSubmitKaggle,
  isSimulating,
  isOptimizing,
  isSubmitting,
}) => {
  return (
    <header id="app-header" className="glass rounded-xl px-6 py-3.5 flex flex-wrap items-center justify-between gap-4 text-white border-b border-white/10 shrink-0 shadow-2xl">
      <div id="brand-container" className="flex items-center space-x-3.5">
        <div id="status-pulse-dot" className="w-3.5 h-3.5 bg-cyan-400 rounded-full pulse shadow-[0_0_12px_rgba(0,210,255,0.9)] shrink-0"></div>
        <div>
          <div className="flex items-center gap-2.5 flex-wrap">
            <h1 id="app-title" className="text-lg font-extrabold tracking-wider text-white uppercase flex items-center gap-2">
              <span className="text-cyan-400">GUGU</span> FARMMIND
            </h1>
            <span id="badge-version" className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30 font-mono font-bold tracking-wider uppercase">
              Autonomous AI Champion
            </span>
          </div>
          <p id="app-bio" className="text-[12px] text-slate-300 font-sans mt-0.5 max-w-xl leading-snug">
            Autonomous decision-intelligence agent engineered for the Kaggle Kaggriculture championship. Powered by hierarchical 720-turn horizon planning, mistake-learning memory, and adaptive market liquidation.
          </p>
        </div>
      </div>

      {/* Real-time Status Badges */}
      <div id="status-badges" className="flex items-center space-x-5 text-[11px] uppercase tracking-wider font-mono">
        <div id="status-kaggle-badge" className="flex flex-col items-end">
          <span className="text-[#8b949e] text-[9px]">Kaggle Rank</span>
          <span className="text-cyan-400 font-bold text-sm glow-text">#{status?.kaggle?.rank || 14} / 1,482</span>
        </div>

        <div id="status-winrate-badge" className="flex flex-col items-end">
          <span className="text-[#8b949e] text-[9px]">Win Rate</span>
          <span className="text-[#00ff9d] font-bold text-sm">
            {status?.champion ? `${(status.champion.win_rate * 100).toFixed(1)}%` : "74.2%"}
          </span>
        </div>

        <div id="status-gemini-badge" className="flex flex-col items-end">
          <span className="text-[#8b949e] text-[9px]">Advisor Model</span>
          <span className="text-white font-medium">gemini-3.6-flash</span>
        </div>
      </div>

      {/* Action Trigger Buttons */}
      <div id="header-action-buttons" className="flex items-center gap-2">
        <button
          id="btn-run-simulation"
          onClick={onRunSimulation}
          disabled={isSimulating}
          className="flex items-center gap-2 bg-white/5 hover:bg-white/10 text-slate-200 px-3.5 py-2 rounded-lg text-[11px] font-bold font-mono uppercase tracking-wider border border-white/10 transition disabled:opacity-50"
        >
          {isSimulating ? <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" /> : <Play className="w-3.5 h-3.5 text-[#00ff9d]" />}
          Run Benchmark
        </button>

        <button
          id="btn-run-optimization"
          onClick={onOptimize}
          disabled={isOptimizing}
          className="flex items-center gap-2 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 px-3.5 py-2 rounded-lg text-[11px] font-bold font-mono uppercase tracking-wider border border-cyan-500/40 shadow-[0_0_12px_rgba(0,210,255,0.2)] transition disabled:opacity-50"
        >
          {isOptimizing ? <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" /> : <Sparkles className="w-3.5 h-3.5 text-cyan-400" />}
          Evolve Strategy
        </button>

        <button
          id="btn-kaggle-submit"
          onClick={onSubmitKaggle}
          disabled={isSubmitting}
          className="flex items-center gap-2 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 px-3.5 py-2 rounded-lg text-[11px] font-bold font-mono uppercase tracking-wider border border-amber-500/40 transition disabled:opacity-50"
        >
          {isSubmitting ? <RefreshCw className="w-3.5 h-3.5 animate-spin text-amber-400" /> : <Send className="w-3.5 h-3.5 text-amber-400" />}
          Package & Submit
        </button>
      </div>
    </header>
  );
};
