import React from "react";
import { TrendingUp, AlertTriangle, Activity, DollarSign } from "lucide-react";
import { MarketCommodity } from "../types";

interface MarketIntelligenceProps {
  marketData: Record<string, MarketCommodity> | null;
}

export const MarketIntelligence: React.FC<MarketIntelligenceProps> = ({ marketData }) => {
  const getRegimeBadge = (regime: string) => {
    switch (regime) {
      case "SCARCITY":
        return "bg-[#00ff9d]/20 text-[#00ff9d] border-[#00ff9d]/30 shadow-[0_0_8px_rgba(0,255,157,0.3)]";
      case "OVERSUPPLY":
        return "bg-amber-500/20 text-amber-300 border-amber-500/30";
      case "PRICE_COLLAPSE":
        return "bg-rose-500/20 text-rose-400 border-rose-500/30";
      case "RECOVERY":
        return "bg-cyan-500/20 text-cyan-400 border-cyan-500/30";
      default:
        return "bg-white/5 text-[#8b949e] border-white/10";
    }
  };

  const commodities: Record<string, MarketCommodity> = marketData || {
    WHEAT: { current_price: 22.0, base_price: 22.0, velocity: 0.5, regime: "NORMAL", forecast_3d: [22.5, 23.0, 22.8] },
    CORN: { current_price: 38.5, base_price: 42.0, velocity: -1.2, regime: "OVERSUPPLY", forecast_3d: [37.0, 36.5, 38.0] },
    TOMATOES: { current_price: 115.0, base_price: 90.0, velocity: 4.8, regime: "SCARCITY", forecast_3d: [120.0, 122.5, 119.0] },
    MILK: { current_price: 24.0, base_price: 24.0, velocity: 0.0, regime: "NORMAL", forecast_3d: [24.0, 24.0, 24.0] },
  };

  return (
    <div id="market-intelligence" className="glass rounded-xl p-6 text-white space-y-4 border border-white/10">
      <div id="market-header" className="flex items-center justify-between">
        <div>
          <h3 id="market-title" className="text-xs uppercase tracking-[0.2em] font-bold text-[#8b949e] flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" />
            Market Dynamics & Regime Forecast
          </h3>
          <p id="market-subtitle" className="text-[11px] text-[#8b949e] font-mono mt-1">
            Price velocity, acceleration, supply elasticity, and town demand regimes.
          </p>
        </div>
      </div>

      <div id="market-cards-grid" className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(commodities).map(([item, rawData]) => {
          const data = rawData as MarketCommodity;
          return (
            <div key={item} id={`market-card-${item}`} className="bg-white/5 border border-white/10 rounded-lg p-4 font-mono">
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-white tracking-wide">{item}</span>
                <span className={`text-[9px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${getRegimeBadge(data.regime)}`}>
                  {data.regime}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs mb-3">
                <div>
                  <span className="text-[#8b949e] text-[10px] uppercase">Current Price:</span>
                  <div className="text-base font-bold text-white">${data.current_price}</div>
                </div>
                <div>
                  <span className="text-[#8b949e] text-[10px] uppercase">Velocity (1d):</span>
                  <div className={data.velocity >= 0 ? "text-[#00ff9d] font-bold" : "text-rose-400 font-bold"}>
                    {data.velocity >= 0 ? `+${data.velocity}` : data.velocity} / day
                  </div>
                </div>
              </div>

              <div className="text-[11px] text-[#8b949e] border-t border-white/10 pt-2 flex justify-between">
                <span>3-Day Forecast:</span>
                <span className="text-cyan-300 font-bold">{data.forecast_3d.map((p) => `$${p}`).join(" → ")}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
