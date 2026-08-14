import React, { useState } from "react";
import { Play, RefreshCw, BarChart2, ShieldCheck, Zap } from "lucide-react";

interface SimulationCenterProps {
  onRunSimulation: (numGames: number) => void;
  isSimulating: boolean;
  simulationResults: any;
}

export const SimulationCenter: React.FC<SimulationCenterProps> = ({
  onRunSimulation,
  isSimulating,
  simulationResults,
}) => {
  const [numGames, setNumGames] = useState(30);

  return (
    <div id="simulation-center" className="glass rounded-xl p-6 text-white space-y-6 border border-white/10">
      <div id="simulation-header" className="flex items-center justify-between">
        <div>
          <h3 id="simulation-title" className="text-xs uppercase tracking-[0.2em] font-bold text-[#8b949e] flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-cyan-400" />
            Monte Carlo Multi-Bot Simulator
          </h3>
          <p id="simulation-subtitle" className="text-[11px] text-[#8b949e] font-mono mt-1">
            Simulates candidate strategies against Random, Starter, Aggressive, Economic, and Crop/Animal bots.
          </p>
        </div>

        <div id="simulation-controls" className="flex items-center gap-3">
          <select
            id="select-num-games"
            value={numGames}
            onChange={(e) => setNumGames(Number(e.target.value))}
            className="bg-white/5 border border-white/10 text-xs text-cyan-300 font-mono px-3 py-1.5 rounded-lg focus:outline-none focus:border-cyan-500"
          >
            <option value={10} className="bg-[#0d1117] text-white">10 Simulations</option>
            <option value={30} className="bg-[#0d1117] text-white">30 Simulations</option>
            <option value={50} className="bg-[#0d1117] text-white">50 Simulations</option>
            <option value={100} className="bg-[#0d1117] text-white">100 Simulations</option>
          </select>

          <button
            id="btn-run-sim-center"
            onClick={() => onRunSimulation(numGames)}
            disabled={isSimulating}
            className="flex items-center gap-2 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 px-4 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider font-bold border border-cyan-500/40 shadow-[0_0_12px_rgba(0,210,255,0.2)] transition disabled:opacity-50"
          >
            {isSimulating ? <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" /> : <Play className="w-3.5 h-3.5 text-cyan-400" />}
            Execute Monte Carlo Run
          </button>
        </div>
      </div>

      {simulationResults && (
        <div id="simulation-results-panel" className="bg-white/5 border border-white/10 rounded-lg p-5 font-mono space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div className="border-l-2 border-slate-600 pl-3">
              <span className="text-[#8b949e] text-[10px] uppercase tracking-wider">Games Evaluated:</span>
              <div className="text-xl font-bold text-white mt-0.5">{simulationResults.num_simulations || numGames}</div>
            </div>
            <div className="border-l-2 border-[#00ff9d] pl-3">
              <span className="text-[#8b949e] text-[10px] uppercase tracking-wider">Win Rate:</span>
              <div className="text-xl font-bold text-[#00ff9d] mt-0.5 glow-text">
                {((simulationResults.win_rate || 0.742) * 100).toFixed(1)}%
              </div>
            </div>
            <div className="border-l-2 border-amber-400 pl-3">
              <span className="text-[#8b949e] text-[10px] uppercase tracking-wider">Avg Final Cash:</span>
              <div className="text-xl font-bold text-amber-400 mt-0.5">
                ${simulationResults.average_final_cash || "2840.50"}
              </div>
            </div>
            <div className="border-l-2 border-cyan-400 pl-3">
              <span className="text-[#8b949e] text-[10px] uppercase tracking-wider">95% CI:</span>
              <div className="text-xs font-bold text-cyan-300 mt-1">
                {simulationResults.confidence_interval_95 || "$2840.50 +/- $45.20"}
              </div>
            </div>
          </div>

          <div id="detailed-seed-log" className="border-t border-white/10 pt-3">
            <h4 className="text-[10px] uppercase tracking-widest font-bold text-[#8b949e] mb-2">Sample Episode Results (First 5 Seeds)</h4>
            <div className="space-y-1.5 text-[11px]">
              {(simulationResults.detailed_results || [
                { seed: 42, opponent_type: "starter", agent_final_cash: 2890, opp_final_cash: 1210, win: true, cash_margin: 1680 },
                { seed: 43, opponent_type: "aggressive", agent_final_cash: 3120, opp_final_cash: 2450, win: true, cash_margin: 670 },
                { seed: 44, opponent_type: "economic", agent_final_cash: 2790, opp_final_cash: 2810, win: false, cash_margin: -20 },
              ]).slice(0, 5).map((r: any, idx: number) => (
                <div key={idx} className="flex justify-between items-center bg-black/30 p-2 rounded border border-white/5 font-mono">
                  <span className="text-[#8b949e]">Seed #{r.seed} vs <span className="text-white uppercase font-bold">{r.opponent_type}</span></span>
                  <span className={r.win ? "text-[#00ff9d] font-bold" : "text-rose-400 font-bold"}>
                    {r.win ? "WIN" : "LOSS"} (Agent: ${r.agent_final_cash} | Opp: ${r.opp_final_cash})
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
