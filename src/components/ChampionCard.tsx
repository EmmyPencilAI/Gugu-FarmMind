import React from "react";
import { Award, DollarSign, TrendingUp, ShieldAlert, BarChart3, CheckCircle2 } from "lucide-react";
import { StrategyConfig } from "../types";

interface ChampionCardProps {
  champion: StrategyConfig | null;
}

export const ChampionCard: React.FC<ChampionCardProps> = ({ champion }) => {
  const winRate = champion ? (champion.win_rate * 100).toFixed(1) : "74.2";
  const avgCash = champion ? champion.average_final_cash.toFixed(2) : "2840.50";

  return (
    <div id="champion-card" className="glass rounded-xl p-6 text-white relative overflow-hidden shadow-2xl border border-white/10">
      <div id="champion-bg-accent" className="absolute top-0 right-0 -mt-10 -mr-10 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div id="champion-header" className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div id="badge-champion-icon" className="w-10 h-10 rounded-lg bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 glow-cyan">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span id="label-champion-status" className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-[#00ff9d]/20 text-[#00ff9d] border border-[#00ff9d]/30 font-mono tracking-wider">
                ACTIVE CHAMPION
              </span>
              <span id="label-champion-version" className="text-xs text-[#8b949e] font-mono">
                {champion?.version || "1.0.0"}
              </span>
            </div>
            <h2 id="champion-title" className="text-lg font-bold text-white mt-0.5 tracking-wide">
              {champion?.name || "Balanced Portfolio Champion v1"}
            </h2>
          </div>
        </div>

        <div id="champion-id-badge" className="text-right text-[11px] font-mono text-[#8b949e]">
          ID: <span className="text-cyan-400">{champion?.strategy_id || "strat_champ_v1"}</span>
        </div>
      </div>

      <p id="champion-description" className="text-xs text-[#8b949e] mb-6 leading-relaxed font-mono">
        {champion?.description || "Baseline Champion model trained on multi-bot simulation suite. Maximizes Expected Final Cash (EFC) and hedges against crop price collapse."}
      </p>

      {/* Grid Metrics */}
      <div id="champion-metrics-grid" className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div id="metric-winrate" className="bg-white/5 border-l-2 border-cyan-400 p-3.5 rounded border border-white/10">
          <div className="flex items-center gap-1.5 text-[10px] text-[#8b949e] uppercase tracking-widest font-mono mb-1">
            <TrendingUp className="w-3.5 h-3.5 text-[#00ff9d]" />
            <span>Win Rate</span>
          </div>
          <div id="val-winrate" className="text-2xl font-bold text-[#00ff9d] font-mono glow-text">
            {winRate}%
          </div>
        </div>

        <div id="metric-avg-cash" className="bg-white/5 border-l-2 border-amber-400 p-3.5 rounded border border-white/10">
          <div className="flex items-center gap-1.5 text-[10px] text-[#8b949e] uppercase tracking-widest font-mono mb-1">
            <DollarSign className="w-3.5 h-3.5 text-amber-400" />
            <span>Avg Final Cash</span>
          </div>
          <div id="val-avg-cash" className="text-2xl font-bold text-amber-400 font-mono">
            ${avgCash}
          </div>
        </div>

        <div id="metric-reserve" className="bg-white/5 border-l-2 border-cyan-400 p-3.5 rounded border border-white/10">
          <div className="flex items-center gap-1.5 text-[10px] text-[#8b949e] uppercase tracking-widest font-mono mb-1">
            <ShieldAlert className="w-3.5 h-3.5 text-cyan-400" />
            <span>Cash Buffer</span>
          </div>
          <div id="val-reserve" className="text-2xl font-bold text-cyan-400 font-mono">
            ${champion?.cash_reserve || 120}
          </div>
        </div>

        <div id="metric-endgame" className="bg-white/5 border-l-2 border-indigo-400 p-3.5 rounded border border-white/10">
          <div className="flex items-center gap-1.5 text-[10px] text-[#8b949e] uppercase tracking-widest font-mono mb-1">
            <BarChart3 className="w-3.5 h-3.5 text-indigo-400" />
            <span>Endgame Trigger</span>
          </div>
          <div id="val-endgame" className="text-2xl font-bold text-indigo-300 font-mono">
            Day {champion?.endgame_threshold || 24}
          </div>
        </div>
      </div>

      {/* Parameter Distribution Sliders */}
      <div id="champion-allocations" className="space-y-3">
        <div>
          <div className="flex justify-between text-[11px] text-[#8b949e] mb-1.5 font-mono uppercase tracking-wider">
            <span>Crop Allocation ({((champion?.crop_allocation || 0.6) * 100).toFixed(0)}%)</span>
            <span>Livestock Allocation ({((champion?.animal_allocation || 0.4) * 100).toFixed(0)}%)</span>
          </div>
          <div id="allocation-bar-container" className="h-2 w-full bg-white/5 rounded-full overflow-hidden flex border border-white/10 p-0.5">
            <div id="bar-crop" style={{ width: `${(champion?.crop_allocation || 0.6) * 100}%` }} className="bg-[#00ff9d] h-full rounded-l shadow-[0_0_8px_#00ff9d]" />
            <div id="bar-animal" style={{ width: `${(champion?.animal_allocation || 0.4) * 100}%` }} className="bg-[#00d2ff] h-full rounded-r shadow-[0_0_8px_#00d2ff]" />
          </div>
        </div>
      </div>
    </div>
  );
};
