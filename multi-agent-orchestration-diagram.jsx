import React, { useState } from "react";

const MultiAgentDiagram = () => {
  const [activeTab, setActiveTab] = useState("query");

  const tabs = {
    build: {
      label: "Building the Graph",
      subtitle: "Extraction Pipeline — Parallel Workers",
      agents: [
        { id: "orch", label: "Orchestrator", sub: "Dependency graph, work partitioning", x: 340, y: 40, w: 160, h: 50, color: "#c9b97a", textColor: "#1a1812" },
        { id: "w1", label: "Worker Agent", sub: "AGOT Ch 1-15", x: 40, y: 150, w: 130, h: 45, color: "#2a3a2a", textColor: "#c8dcc8", border: "#6b8f71" },
        { id: "w2", label: "Worker Agent", sub: "AGOT Ch 16-30", x: 190, y: 150, w: 130, h: 45, color: "#2a3a2a", textColor: "#c8dcc8", border: "#6b8f71" },
        { id: "w3", label: "Worker Agent", sub: "ACOK Ch 1-15", x: 340, y: 150, w: 130, h: 45, color: "#2a3a2a", textColor: "#c8dcc8", border: "#6b8f71" },
        { id: "w4", label: "Worker Agent", sub: "Wiki: Entity pages", x: 490, y: 150, w: 130, h: 45, color: "#2a3a2a", textColor: "#c8dcc8", border: "#6b8f71" },
        { id: "w5", label: "Worker Agent", sub: "Wiki: Year pages", x: 640, y: 150, w: 130, h: 45, color: "#2a3a2a", textColor: "#c8dcc8", border: "#6b8f71" },
      ],
      harness: { label: "Each worker's Harness loads only its assigned scope", y: 230 },
      output: { label: "Validated extractions → merge into unified graph", y: 280 },
      arrows: [
        { x1: 420, y1: 90, x2: 105, y2: 150 },
        { x1: 420, y1: 90, x2: 255, y2: 150 },
        { x1: 420, y1: 90, x2: 405, y2: 150 },
        { x1: 420, y1: 90, x2: 555, y2: 150 },
        { x1: 420, y1: 90, x2: 705, y2: 150 },
      ],
      note: "Pass 1: parallel by chapter · Pass 3: parallel by character · Orchestrator manages dependencies"
    },
    query: {
      label: "Chat Experience",
      subtitle: "Query Decomposition — Specialist Agents",
      agents: [
        { id: "user", label: "User Query", sub: "\"What's converging on Oldtown?\"", x: 270, y: 25, w: 260, h: 40, color: "#1e2535", textColor: "#b8c8e8", border: "#7a8fb5" },
        { id: "router", label: "Router Agent", sub: "Trigger table + entity index", x: 310, y: 100, w: 180, h: 45, color: "#3a2a22", textColor: "#dcc8b8", border: "#c9b97a" },
        { id: "graph", label: "Graph Traversal", sub: "Adjacency list, hub ranking", x: 40, y: 200, w: 150, h: 50, color: "#25202e", textColor: "#c8b8d8", border: "#8b7a9e" },
        { id: "cite", label: "Citation Agent", sub: "Chapter index, references", x: 210, y: 200, w: 150, h: 50, color: "#25202e", textColor: "#c8b8d8", border: "#8b7a9e" },
        { id: "theory", label: "Theory Agent", sub: "Theory index, evidence", x: 380, y: 200, w: 150, h: 50, color: "#25202e", textColor: "#c8b8d8", border: "#8b7a9e" },
        { id: "spoiler", label: "Spoiler Gate", sub: "first_available filter", x: 550, y: 200, w: 150, h: 50, color: "#25202e", textColor: "#c8b8d8", border: "#8b7a9e" },
        { id: "synth", label: "Synthesis Agent", sub: "Composes final answer", x: 280, y: 310, w: 240, h: 45, color: "#1a1812", textColor: "#c9b97a", border: "#c9b97a" },
      ],
      harness: { label: "Each agent loads only its relevant hot/warm memory via the Harness", y: 390 },
      output: null,
      arrows: [
        { x1: 400, y1: 65, x2: 400, y2: 100 },
        { x1: 350, y1: 145, x2: 115, y2: 200 },
        { x1: 380, y1: 145, x2: 285, y2: 200 },
        { x1: 430, y1: 145, x2: 455, y2: 200 },
        { x1: 460, y1: 145, x2: 625, y2: 200 },
        { x1: 115, y1: 250, x2: 340, y2: 310 },
        { x1: 285, y1: 250, x2: 380, y2: 310 },
        { x1: 455, y1: 250, x2: 430, y2: 310 },
        { x1: 625, y1: 250, x2: 480, y2: 310 },
      ],
      note: "No single agent holds the full graph · Each specialist has focused context · Router dispatches based on trigger table"
    },
    compliance: {
      label: "Allvue Compliance",
      subtitle: "Trade Approval — Multi-Agent Workflow",
      agents: [
        { id: "trade", label: "Trade Incoming", sub: "Buy 10k shares ACME Corp, Fund Alpha", x: 240, y: 25, w: 320, h: 40, color: "#1e2535", textColor: "#b8c8e8", border: "#7a8fb5" },
        { id: "orch2", label: "Orchestrator", sub: "Routes to specialist agents", x: 310, y: 100, w: 180, h: 45, color: "#3a2a22", textColor: "#dcc8b8", border: "#c9b97a" },
        { id: "rules", label: "Rules Agent", sub: "Concentration, restricted lists, guidelines", x: 40, y: 200, w: 180, h: 55, color: "#25202e", textColor: "#c8b8d8", border: "#8b7a9e" },
        { id: "context", label: "Context Agent", sub: "Issuer news, credit changes, pending trades", x: 250, y: 200, w: 200, h: 55, color: "#25202e", textColor: "#c8b8d8", border: "#8b7a9e" },
        { id: "risk", label: "Risk Agent", sub: "Sector concentration, duration, credit quality", x: 480, y: 200, w: 200, h: 55, color: "#25202e", textColor: "#c8b8d8", border: "#8b7a9e" },
        { id: "synth2", label: "Synthesis Agent", sub: "Assembles approval package", x: 230, y: 310, w: 340, h: 50, color: "#1a1812", textColor: "#c9b97a", border: "#c9b97a" },
      ],
      harness: { label: "The Harness loads fund-specific rules, portfolio state, and market context per agent", y: 400 },
      output: null,
      arrows: [
        { x1: 400, y1: 65, x2: 400, y2: 100 },
        { x1: 350, y1: 145, x2: 130, y2: 200 },
        { x1: 400, y1: 145, x2: 350, y2: 200 },
        { x1: 450, y1: 145, x2: 580, y2: 200 },
        { x1: 130, y1: 255, x2: 330, y2: 310 },
        { x1: 350, y1: 255, x2: 390, y2: 310 },
        { x1: 580, y1: 255, x2: 470, y2: 310 },
      ],
      note: "Human sees one clean output: pass/fail + risk impact + notes · Says \"approve\" or \"hold\""
    }
  };

  const active = tabs[activeTab];

  return (
    <div style={{
      background: "#0d0d12",
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "24px",
      fontFamily: "'Georgia', serif",
    }}>
      <h1 style={{
        color: "#c9b97a",
        fontSize: "20px",
        fontWeight: "400",
        letterSpacing: "3px",
        marginBottom: "4px",
      }}>
        MULTI-AGENT ORCHESTRATION
      </h1>
      <p style={{
        color: "#777",
        fontSize: "11px",
        letterSpacing: "1px",
        marginBottom: "20px",
      }}>
        THE HARNESS AS CONTEXT MANAGEMENT · ORCHESTRATION AS EXECUTION
      </p>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "8px", marginBottom: "20px" }}>
        {Object.entries(tabs).map(([key, tab]) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            style={{
              background: activeTab === key ? "#c9b97a22" : "transparent",
              border: `1px solid ${activeTab === key ? "#c9b97a" : "#333"}`,
              color: activeTab === key ? "#c9b97a" : "#666",
              padding: "8px 16px",
              borderRadius: "4px",
              fontSize: "11px",
              fontFamily: "'Georgia', serif",
              cursor: "pointer",
              letterSpacing: "0.5px",
              transition: "all 0.2s ease",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Subtitle */}
      <p style={{ color: "#888", fontSize: "13px", marginBottom: "16px", fontStyle: "italic" }}>
        {active.subtitle}
      </p>

      {/* Diagram */}
      <svg viewBox="0 0 800 440" style={{ maxWidth: "800px", width: "100%" }}>
        <defs>
          <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#555" />
          </marker>
        </defs>

        <rect width="800" height="440" fill="#0d0d12" />

        {/* Arrows */}
        {active.arrows.map((a, i) => (
          <line key={i} x1={a.x1} y1={a.y1} x2={a.x2} y2={a.y2}
            stroke="#444" strokeWidth={1.2} markerEnd="url(#arr)" />
        ))}

        {/* Agent nodes */}
        {active.agents.map(agent => (
          <g key={agent.id}>
            <rect
              x={agent.x} y={agent.y} width={agent.w} height={agent.h} rx={5}
              fill={agent.color + "cc"}
              stroke={agent.border || "#555"}
              strokeWidth={1.5}
            />
            <text x={agent.x + agent.w/2} y={agent.y + (agent.sub ? agent.h/2 - 6 : agent.h/2 + 1)}
              textAnchor="middle" dominantBaseline="middle"
              fill={agent.textColor} fontSize="11" fontWeight="600"
              fontFamily="'Georgia', serif"
            >{agent.label}</text>
            {agent.sub && (
              <text x={agent.x + agent.w/2} y={agent.y + agent.h/2 + 9}
                textAnchor="middle" dominantBaseline="middle"
                fill={agent.textColor + "99"} fontSize="8"
                fontFamily="'Georgia', serif"
              >{agent.sub}</text>
            )}
          </g>
        ))}

        {/* Harness bar */}
        <rect x={40} y={active.harness.y} width={720} height={30} rx={4}
          fill="#1a181222" stroke="#c9b97a44" strokeWidth={1} strokeDasharray="4,3" />
        <text x={400} y={active.harness.y + 16} textAnchor="middle"
          fill="#c9b97a88" fontSize="9" fontFamily="'Georgia', serif" fontStyle="italic"
        >
          {active.harness.label}
        </text>

        {/* Note */}
        <text x={400} y={430} textAnchor="middle"
          fill="#555" fontSize="8.5" fontFamily="'Georgia', serif" fontStyle="italic"
        >
          {active.note}
        </text>
      </svg>

      {/* Architecture principle */}
      <div style={{
        background: "#1a1a2e",
        border: "1px solid #c9b97a33",
        borderRadius: "8px",
        padding: "16px 20px",
        maxWidth: "600px",
        marginTop: "20px",
      }}>
        <p style={{ color: "#c9b97a", fontSize: "11px", fontWeight: "600", marginBottom: "8px", letterSpacing: "1px" }}>
          THE COMMON PATTERN
        </p>
        <p style={{ color: "#999", fontSize: "12px", lineHeight: "1.6", margin: 0 }}>
          No single agent can hold everything it needs in one context window.
          Decompose by specialty. Give each agent only its relevant context via the Harness.
          The orchestrator assembles outputs. The Harness is context management.
          Orchestration is execution. They're complementary.
        </p>
      </div>
    </div>
  );
};

export default MultiAgentDiagram;
