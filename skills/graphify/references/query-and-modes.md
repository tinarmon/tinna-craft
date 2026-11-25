# Graphify Query, Path, Explain & Export Subcommands

## 1. `/graphify query "<question>" [--dfs] [--budget N]`
Traverse `graphify-out/graph.json` using BFS (default, depth 3) or DFS (`--dfs`, depth 6):

```powershell
python -c "import json, sys; from pathlib import Path; from networkx.readwrite import json_graph; data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8')); G = json_graph.node_link_graph(data, edges='links'); q = 'QUESTION'; terms = [t.lower() for t in q.split() if len(t) > 2]; scored = sorted([(sum(1 for t in terms if t in G.nodes[n].get('label','').lower()), n) for n in G.nodes()], reverse=True); starts = [n for s, n in scored[:3] if s > 0]; print('Start nodes:', [G.nodes[n].get('label', n) for n in starts]); sub = set(starts); edges = []; frontier = set(starts); [ (next_f := {nb for n in frontier for nb in G.neighbors(n) if nb not in sub}, edges.extend([(n, nb) for n in frontier for nb in G.neighbors(n) if nb not in sub]), sub.update(next_f), frontier := next_f) for _ in range(3) ]; [print('NODE:', G.nodes[n].get('label', n), G.nodes[n].get('source_file','')) for n in sub]; [print('EDGE:', G.nodes[u].get('label',u), '--', G.edges[u,v].get('relation',''), '-->', G.nodes[v].get('label',v)) for u,v in edges]"
```

## 2. `/graphify path "<NodeA>" "<NodeB>"`
Find the shortest path between two concepts in `graphify-out/graph.json`:

```powershell
python -c "import json, networkx as nx; from pathlib import Path; from networkx.readwrite import json_graph; G = json_graph.node_link_graph(json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8')), edges='links'); find = lambda t: max(G.nodes(), key=lambda n: sum(1 for w in t.lower().split() if w in G.nodes[n].get('label','').lower())); p = nx.shortest_path(G, find('NODE_A'), find('NODE_B')); print(' -> '.join(G.nodes[n].get('label', n) for n in p))"
```

## 3. `/graphify explain "<NodeName>"`
Inspect a node's degree, source file, and all immediate neighbors:

```powershell
python -c "import json; from pathlib import Path; from networkx.readwrite import json_graph; G = json_graph.node_link_graph(json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8')), edges='links'); nid = max(G.nodes(), key=lambda n: sum(1 for w in 'NODE_NAME'.lower().split() if w in G.nodes[n].get('label','').lower())); print('Node:', G.nodes[nid]); [print(' ->', G.edges[nid, nb].get('relation',''), G.nodes[nb].get('label', nb)) for nb in G.neighbors(nid)]"
```

## 4. Optional Exports (`--svg`, `--graphml`, `--neo4j`, `--mcp`, `--watch`)
- **SVG**: `from graphify.export import to_svg; to_svg(G, communities, 'graphify-out/graph.svg')`
- **GraphML**: `from graphify.export import to_graphml; to_graphml(G, communities, 'graphify-out/graph.graphml')`
- **Cypher / Neo4j**: `from graphify.export import to_cypher; to_cypher(G, 'graphify-out/cypher.txt')`
- **MCP Server**: `python -m graphify.serve graphify-out/graph.json`
- **File Watcher**: `python -m graphify.watch INPUT_PATH --debounce 3`
