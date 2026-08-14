import React, { useEffect, useState } from "react";
import { Header } from "./components/Header";
import { ChampionCard } from "./components/ChampionCard";
import { StrategyTable } from "./components/StrategyTable";
import { SimulationCenter } from "./components/SimulationCenter";
import { MarketIntelligence } from "./components/MarketIntelligence";
import { OpponentMeta } from "./components/OpponentMeta";
import { GeminiAdvisorPanel } from "./components/GeminiAdvisorPanel";
import { AutonomousControlPanel } from "./components/AutonomousControlPanel";
import { MistakesStream } from "./components/MistakesStream";
import { PlatformStatus, StrategyConfig, MarketCommodity, OpponentProfile, DailyQuotaInfo, MistakeRecord } from "./types";
import { LayoutDashboard, Trophy, GitBranch, BarChart2, Activity, Users, Sparkles, ShieldAlert, Zap } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const [status, setStatus] = useState<PlatformStatus | null>(null);
  const [quota, setQuota] = useState<DailyQuotaInfo | null>(null);
  const [mistakes, setMistakes] = useState<MistakeRecord[]>([]);
  const [strategies, setStrategies] = useState<StrategyConfig[]>([]);
  const [champion, setChampion] = useState<StrategyConfig | null>(null);
  const [marketData, setMarketData] = useState<Record<string, MarketCommodity> | null>(null);
  const [opponents, setOpponents] = useState<OpponentProfile[] | null>(null);

  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [isOptimizing, setIsOptimizing] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [isValidating, setIsValidating] = useState<boolean>(false);

  const [simulationResults, setSimulationResults] = useState<any>(null);
  const [analysisLog, setAnalysisLog] = useState<string | null>(null);
  const [validationResult, setValidationResult] = useState<any>(null);

  const fetchStatus = async () => {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      setStatus(data);
      if (data.quota) {
        setQuota(data.quota);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchQuota = async () => {
    try {
      const res = await fetch("/api/quota");
      const data = await res.json();
      setQuota(data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchMistakes = async () => {
    try {
      const res = await fetch("/api/mistakes");
      const data = await res.json();
      setMistakes(data || []);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchStrategies = async () => {
    try {
      const res = await fetch("/api/strategies");
      const data = await res.json();
      setStrategies(data.all || []);
      setChampion(data.champion || null);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchMarket = async () => {
    try {
      const res = await fetch("/api/market");
      const data = await res.json();
      setMarketData(data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchOpponents = async () => {
    try {
      const res = await fetch("/api/opponents");
      const data = await res.json();
      setOpponents(data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchStatus();
    fetchQuota();
    fetchMistakes();
    fetchStrategies();
    fetchMarket();
    fetchOpponents();

    // Auto refresh status every 4 seconds
    const interval = setInterval(() => {
      fetchStatus();
      fetchQuota();
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  const handleToggleAutonomous = async () => {
    const isCurrentlyRunning = status?.autonomous?.is_running;
    const endpoint = isCurrentlyRunning ? "/api/autonomous/stop" : "/api/autonomous/start";
    try {
      await fetch(endpoint, { method: "POST" });
      fetchStatus();
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunValidation = async () => {
    setIsValidating(true);
    try {
      const res = await fetch("/api/validation/run", { method: "POST" });
      const data = await res.json();
      setValidationResult(data);
      alert(`Validation Episode Result: ${data.status} (Score 1: $${data.agent_clone_score_1}, Score 2: $${data.agent_clone_score_2})`);
    } catch (e) {
      console.error(e);
    } finally {
      setIsValidating(false);
    }
  };

  const handleRunSimulation = async (numGames: number = 35) => {
    setIsSimulating(true);
    try {
      const res = await fetch("/api/simulations/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_games: numGames }),
      });
      const data = await res.json();
      setSimulationResults(data.summary);
      fetchStatus();
      fetchMistakes();
    } catch (e) {
      console.error(e);
    } finally {
      setIsSimulating(false);
    }
  };

  const handleOptimize = async () => {
    setIsOptimizing(true);
    try {
      const res = await fetch("/api/optimize/run", { method: "POST" });
      const data = await res.json();
      fetchStrategies();
      fetchStatus();
      fetchQuota();
      fetchMistakes();
    } catch (e) {
      console.error(e);
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleSubmitKaggle = async () => {
    setIsSubmitting(true);
    try {
      const res = await fetch("/api/kaggle/submit", { method: "POST" });
      const data = await res.json();
      alert(`Kaggle Submission: ${data.submission?.message || "Submitted successfully."}`);
      fetchStatus();
      fetchQuota();
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAnalyzeReplay = async () => {
    setIsAnalyzing(true);
    try {
      const res = await fetch("/api/gemini/analyze", { method: "POST" });
      const data = await res.json();
      setAnalysisLog(data.analysis_log);
      fetchMistakes();
    } catch (e) {
      console.error(e);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div id="app-root" className="min-h-screen bg-[#050608] text-[#c9d1d9] flex flex-col font-sans p-4 md:p-6 space-y-6">
      <Header
        status={status}
        onRunSimulation={() => handleRunSimulation(35)}
        onOptimize={handleOptimize}
        onSubmitKaggle={handleSubmitKaggle}
        isSimulating={isSimulating}
        isOptimizing={isOptimizing}
        isSubmitting={isSubmitting}
      />

      {/* Navigation Tabs */}
      <nav id="nav-tabs" className="glass rounded-xl px-4 flex items-center gap-1 overflow-x-auto text-xs font-mono border border-white/10 shrink-0">
        {[
          { id: "dashboard", label: "Autonomous Control Center", icon: Zap },
          { id: "leaderboard", label: "Ladder & Quota Tracker", icon: Trophy },
          { id: "mistakes", label: "Mistakes & Counter-Evolution", icon: ShieldAlert },
          { id: "strategies", label: "Strategies & Lineage", icon: GitBranch },
          { id: "simulations", label: "Simulation Center", icon: BarChart2 },
          { id: "market", label: "Market Intelligence", icon: Activity },
          { id: "opponents", label: "Opponents & Meta", icon: Users },
          { id: "logs", label: "Gemini Strategic Advisor", icon: Sparkles },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              id={`tab-${tab.id}`}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 py-3 px-4 border-b-2 transition uppercase tracking-wider ${
                isActive
                  ? "border-cyan-400 text-cyan-400 font-bold glow-text bg-cyan-500/10"
                  : "border-transparent text-[#8b949e] hover:text-white hover:bg-white/5"
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* Main Content Body */}
      <main id="main-content" className="flex-1 max-w-7xl mx-auto w-full space-y-6">
        {activeTab === "dashboard" && (
          <div id="view-dashboard" className="space-y-6">
            <AutonomousControlPanel
              status={status}
              quota={quota}
              onToggleAutonomous={handleToggleAutonomous}
              onRunValidation={handleRunValidation}
              isValidating={isValidating}
            />

            <ChampionCard champion={champion} />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <MarketIntelligence marketData={marketData} />
              <OpponentMeta opponents={opponents} />
            </div>

            <MistakesStream mistakes={mistakes} />

            <SimulationCenter
              onRunSimulation={handleRunSimulation}
              isSimulating={isSimulating}
              simulationResults={simulationResults}
            />
          </div>
        )}

        {activeTab === "leaderboard" && (
          <div id="view-leaderboard" className="glass rounded-xl p-6 space-y-6 border border-white/10">
            {/* Daily Quota Banner */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h4 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                  <Trophy className="w-4 h-4 text-amber-400" />
                  Kaggle 24-Hour Submission Quota & Matchmaking Rules
                </h4>
                <p className="text-xs text-slate-400 mt-1">
                  Daily cap: 5 submissions. Only your latest 2 submissions are active on the matchmaking ladder and used for final Bradley-Terry tournament evaluation.
                </p>
              </div>

              <div className="flex items-center gap-4 text-xs font-mono">
                <div className="text-right">
                  <div className="text-amber-400 font-bold">{quota?.used_today ?? 1} / 5 Used Today</div>
                  <div className="text-slate-500">{quota?.remaining_today ?? 4} remaining slots</div>
                </div>
                <div className="text-right pl-4 border-l border-slate-800">
                  <div className="text-cyan-400 font-bold">{quota?.active_ladder_bots?.length ?? 2} Active on Ladder</div>
                  <div className="text-slate-500">Bradley-Terry tracked</div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-xs uppercase tracking-[0.2em] font-bold text-[#8b949e] flex items-center gap-2">
                <Trophy className="w-4 h-4 text-amber-400" />
                Live Ladder Standings & Rating Projection
              </h3>
              <div className="overflow-x-auto font-mono text-xs">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-[#8b949e] uppercase text-[10px] tracking-wider">
                      <th className="p-3">Rank</th>
                      <th className="p-3">Team / Agent</th>
                      <th className="p-3 text-right">Est. Skill Rating (Elo)</th>
                      <th className="p-3 text-right">Avg Final Coins</th>
                      <th className="p-3 text-right">Active Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    <tr className="hover:bg-white/5 transition">
                      <td className="p-3 font-bold text-amber-400">#1</td>
                      <td className="p-3 font-bold text-white">AgriMaster AI</td>
                      <td className="p-3 text-right text-cyan-400 font-bold">1720.5</td>
                      <td className="p-3 text-right text-[#00ff9d] font-bold">$3,420.50</td>
                      <td className="p-3 text-right text-emerald-400">Active (2/2)</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition">
                      <td className="p-3 font-bold text-slate-300">#2</td>
                      <td className="p-3 font-bold text-white">DeepFarm RL</td>
                      <td className="p-3 text-right text-cyan-400 font-bold">1685.0</td>
                      <td className="p-3 text-right text-[#00ff9d] font-bold">$3,310.00</td>
                      <td className="p-3 text-right text-emerald-400">Active (2/2)</td>
                    </tr>
                    <tr className="bg-cyan-500/10 border border-cyan-500/30">
                      <td className="p-3 font-bold text-cyan-400">#14</td>
                      <td className="p-3 font-bold text-cyan-300 flex items-center gap-2">
                        Gugu FarmMind (OURS)
                        <span className="text-[9px] bg-cyan-500/20 text-cyan-400 px-1.5 py-0.5 rounded border border-cyan-500/30 uppercase font-bold">
                          CHAMPION v{champion?.version || "1.0.0"}
                        </span>
                      </td>
                      <td className="p-3 text-right text-cyan-400 font-bold">1568.4</td>
                      <td className="p-3 text-right text-[#00ff9d] font-bold">${champion?.average_final_cash || 2940.5}</td>
                      <td className="p-3 text-right text-cyan-300 font-bold">LADDER SLOT #1</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === "mistakes" && (
          <div id="view-mistakes" className="space-y-6">
            <MistakesStream mistakes={mistakes} />
          </div>
        )}

        {activeTab === "strategies" && (
          <div id="view-strategies" className="space-y-6">
            <StrategyTable strategies={strategies} />
          </div>
        )}

        {activeTab === "simulations" && (
          <div id="view-simulations">
            <SimulationCenter
              onRunSimulation={handleRunSimulation}
              isSimulating={isSimulating}
              simulationResults={simulationResults}
            />
          </div>
        )}

        {activeTab === "market" && (
          <div id="view-market">
            <MarketIntelligence marketData={marketData} />
          </div>
        )}

        {activeTab === "opponents" && (
          <div id="view-opponents">
            <OpponentMeta opponents={opponents} />
          </div>
        )}

        {activeTab === "logs" && (
          <div id="view-logs">
            <GeminiAdvisorPanel
              onAnalyzeReplay={handleAnalyzeReplay}
              isAnalyzing={isAnalyzing}
              analysisLog={analysisLog}
            />
          </div>
        )}
      </main>
    </div>
  );
}
