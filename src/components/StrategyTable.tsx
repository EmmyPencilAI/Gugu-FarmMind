import React from "react";
import { StrategyConfig } from "../types";
import { GitBranch, Shield, Sparkles, AlertCircle } from "lucide-react";

interface StrategyTableProps {
  strategies: StrategyConfig[];
}

export const StrategyTable: React.FC<StrategyTableProps> = ({ strategies }) => {
  const getBadgeStyle = (status: string) => {
    switch (status) {
      case "CHAMPION":
        return "bg-[#00ff9d]/20 text-[#00ff9d] border-[#00ff9d]/30 shadow-[0_0_8px_rgba(0,255,157,0.3)]";
      case "CANDIDATE":
        return "bg-cyan-500/20 text-cyan-400 border-cyan-500/30";
      case "EXPERIMENTAL":
        return "bg-amber-500/20 text-amber-300 border-amber-500/30";
      default:
        return "bg-white/5 text-[#8b949e] border-white/10";
    }
  };

  return (
    <div id="strategy-table-container" className="glass rounded-xl p-6 text-white border border-white/10">
      <div id="strategy-table-header" className="flex items-center justify-between mb-4">
        <div>
          <h3 id="strategy-table-title" className="text-xs uppercase tracking-[0.2em] font-bold text-[#8b949e] flex items-center gap-2">
            <GitBranch className="w-4 h-4 text-cyan-400" />
            Agent Strategy Versioning & Lineage
          </h3>
          <p id="strategy-table-subtitle" className="text-[11px] text-[#8b949e] font-mono mt-1">
            Lifecycle: EXPERIMENTAL → CANDIDATE → CHAMPION → RETIRED. Stronger versions non-destructive.
          </p>
        </div>
      </div>

      <div id="table-wrapper" className="overflow-x-auto">
        <table id="tbl-strategies" className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-white/10 text-[#8b949e] font-mono uppercase text-[10px] tracking-wider">
              <th className="py-2.5 px-3">Status</th>
              <th className="py-2.5 px-3">Strategy ID / Name</th>
              <th className="py-2.5 px-3">Version</th>
              <th className="py-2.5 px-3 text-right">Win Rate</th>
              <th className="py-2.5 px-3 text-right">Avg Final Cash</th>
              <th className="py-2.5 px-3 text-right">Reserve</th>
              <th className="py-2.5 px-3 text-right">Endgame Day</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5 font-mono">
            {strategies.map((strat) => (
              <tr key={strat.strategy_id} id={`row-strat-${strat.strategy_id}`} className="hover:bg-white/5 transition">
                <td className="py-3 px-3">
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${getBadgeStyle(strat.status)}`}>
                    {strat.status}
                  </span>
                </td>
                <td className="py-3 px-3">
                  <div className="font-bold text-white">{strat.name}</div>
                  <div className="text-[10px] text-[#8b949e]">{strat.strategy_id}</div>
                </td>
                <td className="py-3 px-3 text-slate-300">{strat.version}</td>
                <td className="py-3 px-3 text-right text-[#00ff9d] font-bold">
                  {(strat.win_rate * 100).toFixed(1)}%
                </td>
                <td className="py-3 px-3 text-right text-amber-400 font-bold">
                  ${strat.average_final_cash.toFixed(2)}
                </td>
                <td className="py-3 px-3 text-right text-cyan-400">${strat.cash_reserve}</td>
                <td className="py-3 px-3 text-right text-slate-300">Day {strat.endgame_threshold}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
