# Graphify Pipeline Commands Reference (Steps 1–9)

Cross-platform Python commands for executing the full `graphify` build pipeline on Windows PowerShell, macOS, and Linux.

## Step 1: Ensure `graphify` is installed
```powershell
python -c "import graphify" 2>$null; if ($LASTEXITCODE -ne 0) { pip install graphifyy -q }
```

## Step 2: Detect Corpus Files
Replace `INPUT_PATH` with the target directory (default `.`):
```powershell
python -c "import json; from pathlib import Path; from graphify.detect import detect; res = detect(Path('INPUT_PATH')); Path('.graphify_detect.json').write_text(json.dumps(res), encoding='utf-8'); print(f'Total files: {res.get(\"total_files\", 0)}, Words: {res.get(\"total_words\", 0)}')"
```

## Step 3A: Deterministic AST Extraction (Code Files)
```powershell
python -c "import json; from pathlib import Path; from graphify.extract import collect_files, extract; detect = json.loads(Path('.graphify_detect.json').read_text(encoding='utf-8')); code_files = [p for f in detect.get('files', {}).get('code', []) for p in (collect_files(Path(f)) if Path(f).is_dir() else [Path(f)])]; res = extract(code_files) if code_files else {'nodes':[],'edges':[],'input_tokens':0,'output_tokens':0}; Path('.graphify_ast.json').write_text(json.dumps(res, indent=2), encoding='utf-8'); print(f'AST: {len(res[\"nodes\"])} nodes, {len(res[\"edges\"])} edges')"
```

## Step 3B: Semantic Extraction Cache & Subagent Prompt
Check semantic cache first:
```powershell
python -c "import json; from pathlib import Path; from graphify.cache import check_semantic_cache; detect = json.loads(Path('.graphify_detect.json').read_text(encoding='utf-8')); all_files = [f for files in detect['files'].values() for f in files]; cn, ce, uncached = check_semantic_cache(all_files); Path('.graphify_cached.json').write_text(json.dumps({'nodes': cn, 'edges': ce}), encoding='utf-8') if (cn or ce) else None; Path('.graphify_uncached.txt').write_text('\n'.join(uncached), encoding='utf-8'); print(f'Cache hit: {len(all_files)-len(uncached)}, Need extraction: {len(uncached)}')"
```

When `uncached` files include docs/papers/images, split into chunks of 20–25 files and invoke parallel `self` or `research` subagents via `invoke_subagent` with this JSON schema:
```json
{
  "nodes": [{"id": "filestem_entityname", "label": "Human Readable Name", "file_type": "code|document|paper|image", "source_file": "relative/path", "source_location": null, "source_url": null, "captured_at": null, "author": null, "contributor": null}],
  "edges": [{"source": "node_id", "target": "node_id", "relation": "calls|implements|references|cites|conceptually_related_to|shares_data_with|semantically_similar_to", "confidence": "EXTRACTED|INFERRED|AMBIGUOUS", "confidence_score": 1.0, "source_file": "relative/path", "source_location": null, "weight": 1.0}],
  "hyperedges": [],
  "input_tokens": 0,
  "output_tokens": 0
}
```

## Step 3C: Merge AST + Semantic Extractions
```powershell
python -c "import json; from pathlib import Path; ast = json.loads(Path('.graphify_ast.json').read_text(encoding='utf-8')); sem = json.loads(Path('.graphify_semantic.json').read_text(encoding='utf-8')) if Path('.graphify_semantic.json').exists() else {'nodes':[],'edges':[],'input_tokens':0,'output_tokens':0}; seen = {n['id'] for n in ast['nodes']}; merged_nodes = list(ast['nodes']) + [n for n in sem['nodes'] if n['id'] not in seen]; merged = {'nodes': merged_nodes, 'edges': ast['edges'] + sem['edges'], 'input_tokens': sem.get('input_tokens', 0), 'output_tokens': sem.get('output_tokens', 0)}; Path('.graphify_extract.json').write_text(json.dumps(merged, indent=2), encoding='utf-8'); print(f'Merged: {len(merged_nodes)} nodes, {len(merged[\"edges\"])} edges')"
```

## Step 4 & 5: Build Graph, Cluster, Label Communities & Generate Report
```powershell
python -c "import json; from pathlib import Path; from graphify.build import build_from_json; from graphify.cluster import cluster, score_all; from graphify.analyze import god_nodes, surprising_connections, suggest_questions; from graphify.report import generate; from graphify.export import to_json, to_obsidian, to_canvas, to_html; Path('graphify-out').mkdir(exist_ok=True); ext = json.loads(Path('.graphify_extract.json').read_text(encoding='utf-8')); det = json.loads(Path('.graphify_detect.json').read_text(encoding='utf-8')); G = build_from_json(ext); comms = cluster(G); coh = score_all(G, comms); gods = god_nodes(G); surp = surprising_connections(G, comms); labels = {cid: f'Community {cid}' for cid in comms}; qs = suggest_questions(G, comms, labels); rep = generate(G, comms, coh, labels, gods, surp, det, {'input':0,'output':0}, 'INPUT_PATH', suggested_questions=qs); Path('graphify-out/GRAPH_REPORT.md').write_text(rep, encoding='utf-8'); to_json(G, comms, 'graphify-out/graph.json'); to_obsidian(G, comms, 'graphify-out/obsidian', community_labels=labels, cohesion=coh); to_canvas(G, comms, 'graphify-out/obsidian/graph.canvas', community_labels=labels); to_html(G, comms, 'graphify-out/graph.html', community_labels=labels) if G.number_of_nodes() <= 5000 else None; print(f'Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(comms)} communities')"
```

## Step 6: Cleanup Temporary Files
```powershell
python -c "from pathlib import Path; [Path(f).unlink(missing_ok=True) for f in ['.graphify_detect.json','.graphify_extract.json','.graphify_ast.json','.graphify_semantic.json','.graphify_analysis.json','.graphify_labels.json','.graphify_cached.json','.graphify_uncached.txt','.graphify_semantic_new.json']]"
```
