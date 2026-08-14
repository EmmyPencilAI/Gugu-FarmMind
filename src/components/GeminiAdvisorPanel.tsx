import React from "react";
import { Sparkles, RefreshCw, Lightbulb, AlertTriangle, FileCode } from "lucide-react";

interface GeminiAdvisorPanelProps {
  onAnalyzeReplay: () => void;
  isAnalyzing: boolean;
  analysisLog: string | null;
}

export const GeminiAdvisorPanel: React.FC<GeminiAdvisorPanelProps> = ({
  onAnalyzeReplay,
  isAnalyzing,
  analysisLog,
}) => {
  return (
    <div id="gemini-advisor-panel" className="glass rounded-xl p-6 text-white space-y-4 border border-white/10">
      <div id="gemini-header" className="flex items-center justify-between">
        <div>
          <h3 id="gemini-title" className="text-xs uppercase tracking-[0.2em] font-bold text-[#8b949e] flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            Gemini Strategic Intelligence Advisor
          </h3>
          <p id="gemini-subtitle" className="text-[11px] text-[#8b949e] font-mono mt-1">
            Replay diagnostics, failure analysis, and structured parameter hypothesis generation.
          </p>
        </div>

        <button
          id="btn-gemini-analyze-replay"
          onClick={onAnalyzeReplay}
          disabled={isAnalyzing}
          className="flex items-center gap-2 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 px-3.5 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider font-bold border border-cyan-500/40 shadow-[0_0_12px_rgba(0,210,255,0.2)] transition disabled:opacity-50"
        >
          {isAnalyzing ? <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" /> : <Lightbulb className="w-3.5 h-3.5 text-cyan-400" />}
          Run Replay Diagnostic
        </button>
      </div>

      <div id="gemini-log-output" className="bg-black/50 border border-white/10 rounded-lg p-4 font-mono text-xs overflow-x-auto max-h-64 shadow-inner">
        {analysisLog ? (
          <pre id="pre-gemini-log" className="text-cyan-300 whitespace-pre-wrap leading-relaxed">{analysisLog}</pre>
        ) : (
          <div className="text-[#8b949e] space-y-2">
            <p className="text-[#00ff9d]">✓ Strategic Advisor Operational (gemini-3.6-flash).</p>
            <p>• Automated match replay diagnostic ready to synthesize episode logs into parameter mutations.</p>
            <p>• Click "Run Replay Diagnostic" to trigger automated evaluation of recent Kaggle match logs.</p>
          </div>
        )}
      </div>
    </div>
  );
};
