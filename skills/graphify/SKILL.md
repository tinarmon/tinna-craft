---
name: graphify
description: >-
  Use this skill to convert any folder of files (code, docs, papers, images) into a
  navigable knowledge graph with clustered communities, Obsidian vault, interactive HTML,
  GraphRAG-ready JSON, and an honest audit report (`GRAPH_REPORT.md`). Triggers on
  "graphify", "/graphify", "สร้าง knowledge graph", "build knowledge graph", or
  graph queries (`query`, `path`, `explain`).
triggers: graphify, knowledge graph, build knowledge graph, สร้าง knowledge graph, graph report, obsidian vault
---

# Graphify: Multi-Modal Knowledge Graph & Architecture Mapper

Turn any directory of code, docs, PDFs, or images into a persistent knowledge graph (`graphify-out/graph.json`), Obsidian vault (`graphify-out/obsidian/`), interactive HTML (`graphify-out/graph.html`), and audit report (`graphify-out/GRAPH_REPORT.md`).

---

## 1. Supported Commands & Modes

```text
/graphify [path]                        # Full pipeline on directory -> Obsidian + HTML + JSON + Report
/graphify [path] --mode deep            # Thorough extraction with richer INFERRED edges
/graphify [path] --update               # Incremental re-extraction of changed files only
/graphify [path] --cluster-only         # Re-run clustering on existing graph.json
/graphify [path] --no-viz               # Skip Obsidian/HTML visualization (JSON + Report only)
/graphify [path] --svg | --graphml      # Export graph.svg or graph.graphml
/graphify [path] --neo4j                # Export Cypher script for Neo4j
/graphify query "<question>" [--dfs]    # Traverse graph (BFS default, or --dfs) to answer questions
/graphify path "<NodeA>" "<NodeB>"      # Find shortest path between two concepts
/graphify explain "<NodeName>"          # Explain a single node and all its immediate connections
/graphify add <url>                     # Fetch URL into ./raw and incrementally update graph
```

---

## 2. Execution Workflow (Full Pipeline)

When invoked without a path, default to `.` (current working directory). Execute all steps using cross-platform `python` via `run_command`. Full command snippets for each step are located in [pipeline-commands.md](./references/pipeline-commands.md):

1. **Step 1 — Verify Installation:** Check `python -c "import graphify"`, installing `graphifyy` if missing.
2. **Step 2 — Detect Corpus:** Run `graphify.detect` and report file/word counts by category (`code`, `docs`, `papers`, `images`). If `total_files > 200` or `total_words > 2,000,000`, ask the user which subfolder to target first.
3. **Step 3 — Extract Entities & Edges (Parallel AST + Semantic):**
   - **Part A (Code AST):** Run deterministic AST extraction on code files.
   - **Part B (Docs/Papers/Images Semantic):** Check semantic cache first. For uncached non-code files, split into chunks of 20–25 files and dispatch parallel subagents using Antigravity's `invoke_subagent` tool (`TypeName: "self"` or `"research"`). Each edge must be tagged `EXTRACTED` (`1.0`), `INFERRED` (`0.4–0.9`), or `AMBIGUOUS` (`0.1–0.3`).
   - **Part C (Merge):** Combine AST and semantic nodes/edges into `.graphify_extract.json`.
4. **Step 4 & 5 — Build, Cluster & Label Communities:** Build the NetworkX graph, run community detection, assign 2–5 word human-readable community names, and generate `graphify-out/GRAPH_REPORT.md` + `graphify-out/graph.json`.
5. **Step 6 — Generate Visualizations & Clean Up:** Export Obsidian vault (`graphify-out/obsidian/`), Canvas (`graph.canvas`), and interactive HTML (`graphify-out/graph.html`), then unlink temporary `.graphify_*.json` files.
6. **Step 7 — Summary & Guided Navigation:** Present the **God Nodes**, **Surprising Connections**, and **Suggested Questions** from `GRAPH_REPORT.md`, and offer to trace the most cross-cutting question.

---

## 3. Querying, Incremental Updates & Exports

For `/graphify query`, `/graphify path`, `/graphify explain`, `--update`, `--watch`, and `--neo4j` workflows, consult [query-and-modes.md](./references/query-and-modes.md).

---

## 4. Honesty Rules

- **Never invent an edge:** If uncertain, tag as `AMBIGUOUS`.
- **Never skip corpus size warnings** when `total_files > 200` or `total_words > 2,000,000`.
- **Always show raw cohesion scores** and token counts in `GRAPH_REPORT.md`.
- **Skip HTML generation** if node count exceeds `5,000` (use Obsidian vault instead).
