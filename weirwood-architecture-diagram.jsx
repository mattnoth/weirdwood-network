import React, { useState } from "react";

const WeirwoodDiagram = () => {
  const [hoveredNode, setHoveredNode] = useState(null);

  const tooltips = {
    scrape: "~18k JSON files from Playwright scraper. One file per page: {page, html, fetched}. Running on Matt's machine, 6-8 hours.",
    books: "Main five novels + Fire & Blood + TWOIAF + Dunk & Egg. All Tier 1. Split into chapter/section files with YAML frontmatter.",
    discovery: "Classifies every page. Template census, navbox census, reference ID prefixes, section headings, word counts, redlinks. One report, no deletions.",
    parsers: "Type-specific parsers built from discovery report. Entity parser, timeline parser, redirect processor, community page parser, stub parser.",
    edges_wiki: "Untyped: <a> links (page→page). Typed: infobox fields (Combatant, Commander, Orchestrator). Grouping: navbox membership. Source: reference citations.",
    edges_extract: "Family, allegiance, location, possession, co-occurrence, event participation. Typed by LLM extraction against chapter text.",
    edges_later: "Perception (how X sees Y), foreshadowing (moment→event), theory (evidence→claim), reliability (claim→assessment).",
    graph: "Nodes with typed edges. Dual navigation: trigger table (routing) + knowledge graph (traversal). Spoiler-gate-ready via first_available field.",
    alias: "From redirect pages. Maps every alias to canonical entity name. 'The Kingslayer' → 'Jaime Lannister'.",
    adjacency: "Complete link map of the wiki. Inbound counts = hub ranking. Clusters = convergence zones. Link source type preserved.",
    timeline: "From year pages (Events/Births/Deaths) and pre-Conquest consolidated pages. Populates timeline_position field.",
    structured: "Infobox key-value pairs, navbox hierarchies, body text, references with trust-tier-classifiable citation IDs.",
    chapter_data: "Structured extractions per chapter: characters, locations, events, artifacts, information revealed. Schema in Pass 1 agent prompt.",
  };

  const Node = ({ id, x, y, width, height, label, sublabel, color, borderColor, textColor = "#1a1a2e" }) => (
    <g
      onMouseEnter={() => setHoveredNode(id)}
      onMouseLeave={() => setHoveredNode(null)}
      style={{ cursor: "pointer" }}
    >
      <rect
        x={x} y={y} width={width} height={height} rx={6}
        fill={hoveredNode === id ? color : color + "cc"}
        stroke={borderColor || "#555"}
        strokeWidth={hoveredNode === id ? 2.5 : 1.5}
        style={{ transition: "all 0.2s ease" }}
      />
      <text x={x + width/2} y={y + (sublabel ? height/2 - 6 : height/2 + 1)} textAnchor="middle" dominantBaseline="middle"
        fill={textColor} fontSize="11" fontWeight="600" fontFamily="'Georgia', serif"
      >{label}</text>
      {sublabel && (
        <text x={x + width/2} y={y + height/2 + 10} textAnchor="middle" dominantBaseline="middle"
          fill={textColor + "aa"} fontSize="8.5" fontFamily="'Georgia', serif"
        >{sublabel}</text>
      )}
    </g>
  );

  const Arrow = ({ x1, y1, x2, y2, label, dashed, color = "#666" }) => {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len = Math.sqrt(dx*dx + dy*dy);
    const ux = dx/len;
    const uy = dy/len;
    const ax2 = x2 - ux * 6;
    const ay2 = y2 - uy * 6;
    
    return (
      <g>
        <line x1={x1} y1={y1} x2={ax2} y2={ay2}
          stroke={color} strokeWidth={1.2}
          strokeDasharray={dashed ? "4,3" : "none"}
          markerEnd="url(#arrowhead)"
        />
        {label && (
          <text x={(x1+x2)/2 + 8} y={(y1+y2)/2 - 4}
            fill={color} fontSize="7.5" fontFamily="'Georgia', serif"
            fontStyle="italic"
          >{label}</text>
        )}
      </g>
    );
  };

  const SectionLabel = ({ x, y, label, color }) => (
    <g>
      <text x={x} y={y} fill={color || "#8b7355"} fontSize="9" fontWeight="700"
        fontFamily="'Georgia', serif" letterSpacing="1.5" textTransform="uppercase"
      >{label}</text>
      <line x1={x} y1={y + 4} x2={x + label.length * 6.5} y2={y + 4}
        stroke={color || "#8b7355"} strokeWidth={0.8} opacity={0.5}
      />
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
      <h1 style={{
        color: "#c9b97a",
        fontSize: "22px",
        fontWeight: "400",
        letterSpacing: "3px",
        marginBottom: "4px",
        fontFamily: "'Georgia', serif",
      }}>
        THE WEIRWOOD NETWORK
      </h1>
      <p style={{
        color: "#777",
        fontSize: "11px",
        letterSpacing: "1px",
        marginBottom: "20px",
      }}>
        ARCHITECTURE OVERVIEW — PHASE 1 THROUGH KNOWLEDGE GRAPH
      </p>

      <svg viewBox="0 0 780 620" style={{ maxWidth: "780px", width: "100%" }}>
        <defs>
          <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#666" />
          </marker>
          <marker id="arrowhead-gold" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#c9b97a" />
          </marker>
        </defs>

        {/* Background */}
        <rect width="780" height="620" fill="#0d0d12" />

        {/* Phase labels */}
        <SectionLabel x={20} y={30} label="SOURCE CORPUS" color="#6b8f71" />
        <SectionLabel x={20} y={145} label="DISCOVERY" color="#7a8fb5" />
        <SectionLabel x={20} y={245} label="PARSING PIPELINE" color="#b58f7a" />
        <SectionLabel x={20} y={395} label="INTERMEDIATE ARTIFACTS" color="#8b7a9e" />
        <SectionLabel x={20} y={510} label="KNOWLEDGE GRAPH" color="#c9b97a" />

        {/* ═══ SOURCE CORPUS ═══ */}
        <Node id="scrape" x={80} y={45} width={180} height={50}
          label="Wiki Scrape" sublabel="~18k JSON+HTML pages"
          color="#2a3a2a" borderColor="#6b8f71" textColor="#c8dcc8" />
        
        <Node id="books" x={310} y={45} width={180} height={50}
          label="Book Corpus" sublabel="Novels + F&B + TWOIAF + D&E"
          color="#2a3a2a" borderColor="#6b8f71" textColor="#c8dcc8" />

        <Node id="community" x={540} y={45} width={180} height={50}
          label="Community Sources" sublabel="Alt Shift X, Poor Quentyn, SSMs"
          color="#1e2a1e" borderColor="#4a6a4a" textColor="#8aaa8a" />

        {/* ═══ DISCOVERY ═══ */}
        <Node id="discovery" x={180} y={155} width={420} height={55}
          label="Discovery Pass — Classify Everything, Delete Nothing" sublabel="Template census · Navbox census · Ref ID prefixes · Section patterns · Word counts · Redlinks"
          color="#1e2535" borderColor="#7a8fb5" textColor="#b8c8e8" />

        {/* ═══ PARSING PIPELINE ═══ */}
        <Node id="parsers" x={40} y={260} width={140} height={45}
          label="Entity Parser" sublabel="Infobox pages"
          color="#352a22" borderColor="#b58f7a" textColor="#dcc8b8" />
        
        <Node id="timeline_parser" x={195} y={260} width={120} height={45}
          label="Timeline Parser" sublabel="Year pages"
          color="#352a22" borderColor="#b58f7a" textColor="#dcc8b8" />

        <Node id="redirect_parser" x={330} y={260} width={120} height={45}
          label="Redirect Parser" sublabel="Alias pages"
          color="#352a22" borderColor="#b58f7a" textColor="#dcc8b8" />

        <Node id="community_parser" x={465} y={260} width={130} height={45}
          label="Community Parser" sublabel="Meta pages, DYK"
          color="#352a22" borderColor="#b58f7a" textColor="#dcc8b8" />

        <Node id="chapter_parser" x={610} y={260} width={130} height={45}
          label="Chapter Extractor" sublabel="Pass 1: Mechanical"
          color="#352a22" borderColor="#b58f7a" textColor="#dcc8b8" />

        {/* Parser outputs label */}
        <text x={390} y={330} textAnchor="middle" fill="#666" fontSize="8" fontFamily="'Georgia', serif"
          fontStyle="italic">each parser produces typed output</text>

        {/* ═══ EDGE SOURCES ═══ */}
        <rect x={30} y={345} width={720} height={40} rx={4}
          fill="#1a1520" stroke="#8b7a9e" strokeWidth={1} strokeDasharray="3,3" />
        <text x={390} y={362} textAnchor="middle" fill="#8b7a9e" fontSize="9" fontWeight="600"
          fontFamily="'Georgia', serif" letterSpacing="1">
          EDGE SOURCES — connections accumulate across every pass
        </text>
        <text x={390} y={375} textAnchor="middle" fill="#6b5a7e" fontSize="7.5"
          fontFamily="'Georgia', serif">
          Wiki links (untyped) → Infobox fields (typed) → Chapter extraction (relationship) → Voice/Perception → Foreshadowing → Theory
        </text>

        {/* ═══ INTERMEDIATE ARTIFACTS ═══ */}
        <Node id="alias" x={40} y={410} width={120} height={40}
          label="Alias Table" sublabel="name → canonical"
          color="#25202e" borderColor="#8b7a9e" textColor="#c8b8d8" />

        <Node id="adjacency" x={175} y={410} width={130} height={40}
          label="Link Adjacency" sublabel="hub ranking, clusters"
          color="#25202e" borderColor="#8b7a9e" textColor="#c8b8d8" />

        <Node id="timeline" x={320} y={410} width={120} height={40}
          label="Timeline Data" sublabel="events, births, deaths"
          color="#25202e" borderColor="#8b7a9e" textColor="#c8b8d8" />

        <Node id="structured" x={455} y={410} width={140} height={40}
          label="Structured Entities" sublabel="infobox data, navboxes, refs"
          color="#25202e" borderColor="#8b7a9e" textColor="#c8b8d8" />

        <Node id="chapter_data" x={610} y={410} width={140} height={40}
          label="Chapter Extractions" sublabel="Pass 1 structured output"
          color="#25202e" borderColor="#8b7a9e" textColor="#c8b8d8" />

        {/* ═══ KNOWLEDGE GRAPH ═══ */}
        <rect x={120} y={520} width={540} height={80} rx={8}
          fill="#1a1812" stroke="#c9b97a" strokeWidth={2} />
        
        <text x={390} y={545} textAnchor="middle" fill="#c9b97a" fontSize="14" fontWeight="600"
          fontFamily="'Georgia', serif" letterSpacing="1">
          KNOWLEDGE GRAPH
        </text>
        <text x={260} y={568} textAnchor="middle" fill="#a89860" fontSize="9"
          fontFamily="'Georgia', serif">
          Nodes (typed entities)
        </text>
        <text x={390} y={568} textAnchor="middle" fill="#a89860" fontSize="9"
          fontFamily="'Georgia', serif">
          Edges (typed relationships)
        </text>
        <text x={520} y={568} textAnchor="middle" fill="#a89860" fontSize="9"
          fontFamily="'Georgia', serif">
          Trigger Table (routing)
        </text>
        <text x={390} y={585} textAnchor="middle" fill="#776830" fontSize="8"
          fontFamily="'Georgia', serif" fontStyle="italic">
          first_available · timeline_position · narrator_bias · trust_tier
        </text>

        {/* ═══ ARROWS ═══ */}
        {/* Source → Discovery */}
        <Arrow x1={170} y1={95} x2={300} y2={155} />
        <Arrow x1={400} y1={95} x2={400} y2={155} />

        {/* Discovery → Parsers */}
        <Arrow x1={250} y1={210} x2={110} y2={260} label="routes to" />
        <Arrow x1={320} y1={210} x2={255} y2={260} />
        <Arrow x1={390} y1={210} x2={390} y2={260} />
        <Arrow x1={460} y1={210} x2={530} y2={260} />

        {/* Books → Chapter Extractor */}
        <Arrow x1={490} y1={82} x2={675} y2={260} dashed />

        {/* Community → later (dashed) */}
        <Arrow x1={630} y1={95} x2={630} y2={155} dashed color="#4a6a4a" />

        {/* Parsers → Intermediate */}
        <Arrow x1={110} y1={305} x2={100} y2={410} />
        <Arrow x1={255} y1={305} x2={240} y2={410} />
        <Arrow x1={390} y1={305} x2={100} y2={410} />
        <Arrow x1={255} y1={305} x2={380} y2={410} />
        <Arrow x1={110} y1={305} x2={525} y2={410} />
        <Arrow x1={675} y1={305} x2={680} y2={410} />

        {/* Intermediate → Graph */}
        <Arrow x1={100} y1={450} x2={250} y2={520} color="#c9b97a" />
        <Arrow x1={240} y1={450} x2={320} y2={520} color="#c9b97a" />
        <Arrow x1={380} y1={450} x2={370} y2={520} color="#c9b97a" />
        <Arrow x1={525} y1={450} x2={430} y2={520} color="#c9b97a" />
        <Arrow x1={680} y1={450} x2={530} y2={520} color="#c9b97a" />

        {/* Edge sources → Graph */}
        <Arrow x1={390} y1={385} x2={390} y2={520} color="#8b7a9e" />
      </svg>

      {/* Tooltip */}
      {hoveredNode && tooltips[hoveredNode] && (
        <div style={{
          background: "#1a1a2e",
          border: "1px solid #c9b97a44",
          borderRadius: "6px",
          padding: "12px 16px",
          maxWidth: "420px",
          color: "#bbb",
          fontSize: "12px",
          lineHeight: "1.5",
          marginTop: "12px",
          fontFamily: "'Georgia', serif",
        }}>
          {tooltips[hoveredNode]}
        </div>
      )}

      {/* Legend */}
      <div style={{
        display: "flex",
        gap: "24px",
        marginTop: "16px",
        flexWrap: "wrap",
        justifyContent: "center",
      }}>
        {[
          { color: "#6b8f71", label: "Source Corpus" },
          { color: "#7a8fb5", label: "Discovery" },
          { color: "#b58f7a", label: "Parsers" },
          { color: "#8b7a9e", label: "Artifacts & Edges" },
          { color: "#c9b97a", label: "Knowledge Graph" },
        ].map(({ color, label }) => (
          <div key={label} style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <div style={{ width: "10px", height: "10px", borderRadius: "2px", background: color }} />
            <span style={{ color: "#777", fontSize: "10px", fontFamily: "'Georgia', serif" }}>{label}</span>
          </div>
        ))}
      </div>

      <p style={{
        color: "#555",
        fontSize: "9px",
        marginTop: "12px",
        fontStyle: "italic",
        fontFamily: "'Georgia', serif",
      }}>
        Tap any node for details · Dashed lines = future/later phases · Community sources feed into Pass 5+ (Theory Integration)
      </p>
    </div>
  );
};

export default WeirwoodDiagram;
