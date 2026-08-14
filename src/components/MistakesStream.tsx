import React from "react";
import { AlertOctagon, TrendingUp, CheckCircle, ShieldAlert, Sparkles } from "lucide-react";
import { MistakeRecord } from "../types";

interface Props {
  mistakes: MistakeRecord[];
}

export const MistakesStream: React.FC<Props> = ({ mistakes }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-rose-400" />
          <h3 className="text-lg font-bold text-slate-100">Mistakes Memory & Counter-Evolution Stream</h3>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
          {mistakes.length} Strategic Failures Analyzed & Neutralized
        </span>
      </div>

      <p className="text-sm text-slate-400">
        Every simulation loss is automatically decomposed to identify the exact turn of failure, price regime collapse, or opponent pacing deficit. Generational mutations counter these specific failure patterns.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
        {mistakes.map((m, idx) => (
          <div key={idx} className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-3">
            <div className="flex items-start justify-between gap-2">
              <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                {m.failure_category}
              </span>
              <span className="text-xs text-slate-500 font-mono">
                Failed Turn {m.turn_failed * 24} (Day {m.turn_failed})
              </span>
            </div>

            <div>
              <div className="text-xs font-semibold text-slate-300">Root Cause Observed:</div>
              <div className="text-xs text-slate-400 mt-0.5">{m.root_cause}</div>
            </div>

            <div className="p-2.5 rounded bg-emerald-950/30 border border-emerald-800/40 text-xs">
              <div className="flex items-center gap-1.5 text-emerald-400 font-semibold mb-0.5">
                <CheckCircle className="w-3.5 h-3.5" />
                Evolutionary Counter-Measure:
              </div>
              <div className="text-slate-300">{m.counter_action_taken}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
