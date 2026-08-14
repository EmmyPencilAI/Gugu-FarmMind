import React, { useEffect, useState } from "react";
import { Header } from "./components/Header";
import { ChampionCard } from "./components/ChampionCard";
import { StrategyTable } from "./components/StrategyTable";
import { SimulationCenter } from "./components/SimulationCenter";
import { MarketIntelligence } from "./components/MarketIntelligence";
import { OpponentMeta } from "./components/OpponentMeta";
import { GeminiAdvisorPanel } from "./components/GeminiAdvisorPanel";
import { PlatformStatus, StrategyConfig, MarketCommodity, OpponentProfile } from "./types";
import { LayoutDashboard, Trophy, GitBranch, BarChart2, Activity, Users, Sparkles } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const [status, setStatus] = useState<PlatformStatus | null>(null);
  const [strategies, setStrategies] = useState<StrategyConfig[]>([]);
  const [champion, setChampion] = useState<StrategyConfig | null>(null);
  const [marketData, setMarketData] = useState<Record<string, MarketCommodity> | null>(null);
  const [opponents, setOpponents] = useState<OpponentProfile[] | null>(null);

  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [isOptimizing, setIsOptimizing] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  const [simulationResults, setSimulationResults] = useState<any>(null);
  const [analysisLog, setAnalysisLog] = useState<string | null>(null);

  const fetchStatus = async () => {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      setStatus(data);
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
    fetchStrategies();
    fetchMarket();
    fetchOpponents();
  }, []);

  const handleRunSimulation = async (numGames: number = 30) => {
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
      alert(`Kaggle Submission Complete: ${data.submission?.message || "Queued successfully"}`);
      fetchStatus();
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
        onRunSimulation={() => handleRunSimulation(30)}
        onOptimize={handleOptimize}
        onSubmitKaggle={handleSubmitKaggle}
        isSimulating={isSimulating}
        isOptimizing={isOptimizing}
        isSubmitting={isSubmitting}
      />

      {/* Navigation Tabs */}
      <nav id="nav-tabs" className="glass rounded-xl px-4 flex items-center gap-1 overflow-x-auto text-xs font-mono border border-white/10 shrink-0">
        {[
          { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
          { id: "leaderboard", label: "Leaderboard & Submissions", icon: Trophy },
          { id: "strategies", label: "Strategies & Lineage", icon: GitBranch },
          { id: "simulations", label: "Simulation Center", icon: BarChart2 },
          { id: "market", label: "Market Intelligence", icon: Activity },
          { id: "opponents", label: "Opponents & Meta", icon: Users },
          { id: "logs", label: "Gemini Advisor", icon: Sparkles },
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
            <ChampionCard champion={champion} />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <MarketIntelligence marketData={marketData} />
              <OpponentMeta opponents={opponents} />
            </div>

            <SimulationCenter
              onRunSimulation={handleRunSimulation}
              isSimulating={isSimulating}
              simulationResults={simulationResults}
            />
          </div>
        )}

        {activeTab === "leaderboard" && (
          <div id="view-leaderboard" className="glass rounded-xl p-6 space-y-4 border border-white/10">
            <h3 className="text-xs uppercase tracking-[0.2em] font-bold text-[#8b949e] flex items-center gap-2">
              <Trophy className="w-4 h-4 text-amber-400" />
              Kaggriculture 2026 Competition Leaderboard
            </h3>
            <div className="overflow-x-auto font-mono text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-[#8b949e] uppercase text-[10px] tracking-wider">
                    <th className="p-3">Rank</th>
                    <th className="p-3">Team Name</th>
                    <th className="p-3 text-right">Score / Cash</th>
                    <th className="p-3 text-right">Entries</th>
                    <th className="p-3 text-right">Last Submission</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  <tr className="hover:bg-white/5 transition">
                    <td className="p-3 font-bold text-amber-400">#1</td>
                    <td className="p-3 font-bold text-white">AgriMaster AI</td>
                    <td className="p-3 text-right text-[#00ff9d] font-bold">$3,420.50</td>
                    <td className="p-3 text-right text-slate-300">42</td>
                    <td className="p-3 text-right text-[#8b949e]">2 hours ago</td>
                  </tr>
                  <tr className="hover:bg-white/5 transition">
                    <td className="p-3 font-bold text-slate-300">#2</td>
                    <td className="p-3 font-bold text-white">DeepFarm RL</td>
                    <td className="p-3 text-right text-[#00ff9d] font-bold">$3,310.00</td>
                    <td className="p-3 text-right text-slate-300">28</td>
                    <td className="p-3 text-right text-[#8b949e]">5 hours ago</td>
                  </tr>
                  <tr className="bg-cyan-500/10 border border-cyan-500/30">
                    <td className="p-3 font-bold text-cyan-400">#14</td>
                    <td className="p-3 font-bold text-cyan-300 flex items-center gap-2">
                      Autonomous Kaggriculture Engine (OURS)
                      <span className="text-[9px] bg-cyan-500/20 text-cyan-400 px-1.5 py-0.5 rounded border border-cyan-500/30 uppercase font-bold">ACTIVE</span>
                    </td>
                    <td className="p-3 text-right text-[#00ff9d] font-bold">$2,840.50</td>
                    <td className="p-3 text-right text-white">8</td>
                    <td className="p-3 text-right text-cyan-300">Just now</td>
                  </tr>
                </tbody>
              </table>
            </div>
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
