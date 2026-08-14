import React from "react";
import { Users, Crosshair, ShieldAlert, Award } from "lucide-react";
import { OpponentProfile } from "../types";

interface OpponentMetaProps {
  opponents: OpponentProfile[] | null;
}

export const OpponentMeta: React.FC<OpponentMetaProps> = ({ opponents }) => {
  const oppList = opponents || [
    { opponent_id: "AgriMaster_Bot", classification: "AGGRESSIVE_EXPANDER", win_rate_vs_us: 0.28, weaknesses: ["CRITICAL_CASH_STARVATION"], counter_tactics: "Undercut with fast Wheat turnover cycles." },
    { opponent_id: "DeepFarm_RL", classification: "CROP_SPECIALIST", win_rate_vs_us: 0.22, weaknesses: ["MONO_CROP_DEPENDENCE_CORN"], counter_tactics: "Pivot to livestock Milk & Wool for non-correlated income." },
    { opponent_id: "MonoCrop_Bot", classification: "ECONOMIC_HOARDER", win_rate_vs_us: 0.12, weaknesses: ["IDLE_LAND_INEFFICIENCY"], counter_tactics: "Capitalize on land expansion and market scarcity." }
  ];

  return (
    <div id="opponent-meta-container" className="glass rounded-xl p-6 text-white space-y-4 border border-white/10">
      <div id="opponent-header" className="flex items-center justify-between">
        <div>
          <h3 id="opponent-title" className="text-xs uppercase tracking-[0.2em] font-bold text-[#8b949e] flex items-center gap-2">
            <Users className="w-4 h-4 text-cyan-400" />
            Competitive Opponent Meta-Database
          </h3>
          <p id="opponent-subtitle" className="text-[11px] text-[#8b949e] font-mono mt-1">
            Classification of opponent farm archetypes and counter-tactic recommendations.
          </p>
        </div>
      </div>

      <div id="opponents-list" className="space-y-3 font-mono">
        {oppList.map((opp) => (
          <div key={opp.opponent_id} id={`opp-card-${opp.opponent_id}`} className="bg-white/5 border border-white/10 rounded-lg p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-bold text-white flex items-center gap-2 tracking-wide">
                <Crosshair className="w-4 h-4 text-rose-400" />
                {opp.opponent_id}
              </span>
              <span className="text-[9px] font-bold bg-cyan-500/20 text-cyan-400 px-2 py-0.5 rounded border border-cyan-500/30 uppercase tracking-wider">
                {opp.classification}
              </span>
            </div>

            <p className="text-xs text-slate-300 mb-3 leading-relaxed">
              <span className="text-[#8b949e] uppercase text-[10px]">Counter Strategy:</span> {opp.counter_tactics}
            </p>

            <div className="flex justify-between items-center text-[11px] text-[#8b949e] border-t border-white/10 pt-2">
              <span>Vulnerabilities: <span className="text-rose-400 font-bold">{opp.weaknesses.join(", ")}</span></span>
              <span>Win Rate vs Us: <span className="text-amber-400 font-bold">{(opp.win_rate_vs_us * 100).toFixed(0)}%</span></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
