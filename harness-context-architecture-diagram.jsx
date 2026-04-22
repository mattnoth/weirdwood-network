import React, { useState } from "react";

const HarnessDiagram = () => {
  const [hoveredNode, setHoveredNode] = useState(null);

  const tips = {
    query: "Natural language input from user or system event (trade, bug, question about ASOIAF)",
    trigger: "Keyword → domain routing. Maps the query to the right context neighborhood. Same pattern at Allvue and Weirwood Network.",
    hot: "Always loaded. Navigational infrastructure: trigger table, hub ranking, entity index, alias table. Small footprint, always useful.",
    warm: "Loaded per query. Target node + first-degree edges. Filtered by type and relevance. Manageable even for hub nodes.",
    cold: "On demand. Second-degree connections, full chapter text, theory evidence, voice profiles. Only when deep traversal needed.",
    agent: "Specialist agent with focused context window. Only sees what the Harness loads for this query. Multiple agents can run in parallel.",
    graph: "Optional. Markdown works for single-node lookups. Graph DB (Neo4j, SQLite) for multi-hop traversal queries. The Harness sits on top — routing doesn't change.",
    markdown: "Current implementation. Portable, version-controlled, LLM-native. Works for Allvue's deep-but-narrow access pattern.",
    graphdb: "Future option. For queries like 'which characters visited both Oldtown and the Wall' — multi-node traversal with edge filtering.",
    response: "Synthesized answer with provenance. Trust tier, confidence, source citations. Agent can express uncertainty based on metadata.",
  };

  const Node = ({ id, x, y, w, h, label, sub, color, border, textColor = "#ccc" }) => (
    <g onMouseEnter={() => setHoveredNode(id)} onMouseLeave={() => setHoveredNode(null)} style={{ cursor: "pointer" }}>
      <rect x={x} y={y} width={w} height={h} rx={5}
        fill={hoveredNode === id ? color : color + "bb"}
        stroke={border || "#444"} strokeWidth={hoveredNode === id ? 2.5 : 1.5}
        style={{ transition: "all 0.2s" }}
      />
      <text x={x+w/2} y={y + (sub ? h/2-7 : h/2)} textAnchor="middle" dominantBaseline="middle"
        fill={textColor} fontSize="11" fontWeight="600" fontFamily="'Georgia', serif"
      >{label}</text>
      {sub && <text x={x+w/2} y={y+h/2+9} textAnchor="middle" dominantBaseline="middle"
        fill={textColor+"99"} fontSize="8" fontFamily="'Georgia', serif">{sub}</text>}
    </g>
  );

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
      <h1 style={{ color: "#c9b97a", fontSize: "20px", fontWeight: "400", letterSpacing: "3px", marginBottom: "4px" }}>
        THE HARNESS — CONTEXT ARCHITECTURE
      </h1>
      <p style={{ color: "#777", fontSize: "11px", letterSpacing: "1px", marginBottom: "20px" }}>
        ROUTING · MEMORY TIERS · STORAGE BACKENDS · AGENT CONTEXT MANAGEMENT
      </p>

      <svg viewBox="0 0 700 520" style={{ maxWidth: "700px", width: "100%" }}>
        <rect width="700" height="520" fill="#0d0d12" />
        <defs>
          <marker id="a1" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#555" />
          </marker>
          <marker id="a2" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#c9b97a" />
          </marker>
        </defs>

        {/* Section labels */}
        <text x={20} y={28} fill="#7a8fb5" fontSize="8" fontWeight="700" letterSpacing="1.5" fontFamily="'Georgia', serif">INPUT</text>
        <text x={20} y={98} fill="#c9b97a" fontSize="8" fontWeight="700" letterSpacing="1.5" fontFamily="'Georgia', serif">ROUTING LAYER</text>
        <text x={20} y={178} fill="#8b7a9e" fontSize="8" fontWeight="700" letterSpacing="1.5" fontFamily="'Georgia', serif">MEMORY TIERS</text>
        <text x={20} y={348} fill="#6b8f71" fontSize="8" fontWeight="700" letterSpacing="1.5" fontFamily="'Georgia', serif">STORAGE BACKENDS</text>
        <text x={20} y={438} fill="#b58f7a" fontSize="8" fontWeight="700" letterSpacing="1.5" fontFamily="'Georgia', serif">OUTPUT</text>

        {/* Query */}
        <Node id="query" x={230} y={35} w={240} h={40} label="Query / Event" sub="natural language input"
          color="#1e2535" border="#7a8fb5" textColor="#b8c8e8" />

        {/* Trigger Table */}
        <Node id="trigger" x={200} y={108} w={300} h={45} label="Trigger Table / Taxonomy"
          sub="keyword → domain routing · scopes context loading"
          color="#2a2518" border="#c9b97a" textColor="#e8d8a8" />

        {/* Memory Tiers */}
        <Node id="hot" x={40} y={195} w={190} h={65} label="HOT MEMORY"
          sub="Always loaded · Trigger table, hub index, aliases, entity types"
          color="#2a1818" border="#cc6666" textColor="#e8b8b8" />
        <Node id="warm" x={255} y={195} w={190} h={65} label="WARM MEMORY"
          sub="Per query · Target node + first-degree edges, filtered by type"
          color="#2a2518" border="#ccaa44" textColor="#e8d8a8" />
        <Node id="cold" x={470} y={195} w={190} h={65} label="COLD MEMORY"
          sub="On demand · Deep traversal, full text, theories, evidence chains"
          color="#182a2a" border="#44aacc" textColor="#a8d8e8" />

        {/* Agent */}
        <Node id="agent" x={220} y={290} w={260} h={40} label="Specialist Agent"
          sub="focused context window · sees only what the Harness loads"
          color="#25202e" border="#8b7a9e" textColor="#c8b8d8" />

        {/* Storage backends */}
        <Node id="markdown" x={100} y={365} w={200} h={50} label="Markdown Files"
          sub="Portable, version-controlled, LLM-native · Single-node lookups"
          color="#1e2a1e" border="#6b8f71" textColor="#c8dcc8" />
        <Node id="graphdb" x={400} y={365} w={200} h={50} label="Graph DB (optional)"
          sub="Neo4j / SQLite · Multi-hop traversal, edge filtering"
          color="#1e2a1e" border="#6b8f71" textColor="#c8dcc8" />

        {/* "OR" connector */}
        <text x={350} y={393} textAnchor="middle" fill="#6b8f71" fontSize="10" fontWeight="600"
          fontFamily="'Georgia', serif">or</text>

        {/* Response */}
        <Node id="response" x={200} y={445} w={300} h={45} label="Response with Provenance"
          sub="trust tier · confidence · source citations · uncertainty expressed"
          color="#2a2218" border="#b58f7a" textColor="#dcc8b8" />

        {/* Arrows */}
        <line x1={350} y1={75} x2={350} y2={108} stroke="#555" strokeWidth={1.2} markerEnd="url(#a1)" />
        <line x1={270} y1={153} x2={135} y2={195} stroke="#c9b97a" strokeWidth={1} markerEnd="url(#a2)" />
        <line x1={350} y1={153} x2={350} y2={195} stroke="#c9b97a" strokeWidth={1} markerEnd="url(#a2)" />
        <line x1={430} y1={153} x2={565} y2={195} stroke="#c9b97a" strokeWidth={1} markerEnd="url(#a2)" />
        
        <line x1={135} y1={260} x2={300} y2={290} stroke="#555" strokeWidth={1} markerEnd="url(#a1)" />
        <line x1={350} y1={260} x2={350} y2={290} stroke="#555" strokeWidth={1} markerEnd="url(#a1)" />
        <line x1={565} y1={260} x2={400} y2={290} stroke="#555" strokeWidth={1} markerEnd="url(#a1)" />

        <line x1={300} y1={330} x2={200} y2={365} stroke="#555" strokeWidth={1} markerEnd="url(#a1)" strokeDasharray="4,3" />
        <line x1={400} y1={330} x2={500} y2={365} stroke="#555" strokeWidth={1} markerEnd="url(#a1)" strokeDasharray="4,3" />

        <line x1={200} y1={415} x2={300} y2={445} stroke="#555" strokeWidth={1} markerEnd="url(#a1)" />
        <line x1={500} y1={415} x2={400} y2={445} stroke="#555" strokeWidth={1} markerEnd="url(#a1)" />
      </svg>

      {/* Tooltip */}
      {hoveredNode && tips[hoveredNode] && (
        <div style={{
          background: "#1a1a2e",
          border: "1px solid #c9b97a44",
          borderRadius: "6px",
          padding: "12px 16px",
          maxWidth: "500px",
          color: "#bbb",
          fontSize: "12px",
          lineHeight: "1.5",
          marginTop: "12px",
        }}>
          {tips[hoveredNode]}
        </div>
      )}

      {/* Comparison */}
      <div style={{
        display: "flex",
        gap: "16px",
        marginTop: "20px",
        maxWidth: "700px",
        width: "100%",
      }}>
        <div style={{
          flex: 1,
          background: "#1a1812",
          border: "1px solid #c9b97a33",
          borderRadius: "8px",
          padding: "14px 16px",
        }}>
          <p style={{ color: "#c9b97a", fontSize: "10px", fontWeight: "700", letterSpacing: "1px", marginBottom: "6px" }}>
            ALLVUE (CURRENT)
          </p>
          <p style={{ color: "#888", fontSize: "11px", lineHeight: "1.5", margin: 0 }}>
            Deep but narrow. One topic at a time. Markdown files. Single-node lookups. The Harness routes to the right doc and loads it. This works.
          </p>
        </div>
        <div style={{
          flex: 1,
          background: "#1a1820",
          border: "1px solid #8b7a9e33",
          borderRadius: "8px",
          padding: "14px 16px",
        }}>
          <p style={{ color: "#8b7a9e", fontSize: "10px", fontWeight: "700", letterSpacing: "1px", marginBottom: "6px" }}>
            WEIRWOOD / COMPLIANCE (FUTURE)
          </p>
          <p style={{ color: "#888", fontSize: "11px", lineHeight: "1.5", margin: 0 }}>
            Wide and interconnected. Multi-hop traversal. Graph DB underneath, Harness on top. Same routing pattern, new traversal capability. The architecture extends.
          </p>
        </div>
      </div>

      <p style={{ color: "#555", fontSize: "9px", marginTop: "16px", fontStyle: "italic" }}>
        Tap any node for details · Dashed lines = storage backend is interchangeable · The Harness pattern is the same regardless of backend
      </p>
    </div>
  );
};

export default HarnessDiagram;
