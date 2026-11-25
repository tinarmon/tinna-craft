"""Render a feature-and-test-case JSON tree into Mermaid and an offline interactive HTML report."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

VALID_STATUSES = {"covered", "missing"}


def _safe_id(raw: str, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", raw).strip("_")
    return cleaned or fallback


def _mermaid_label(text: str) -> str:
    """Escape characters that break Mermaid node labels."""
    return (
        text.replace('"', "'")
        .replace("[", "(")
        .replace("]", ")")
        .replace("{", "(")
        .replace("}", ")")
        .replace("\n", " ")
        .strip()
    )


def compute_stats(data: dict[str, Any]) -> dict[str, Any]:
    """Compute per-feature and overall test coverage counts."""
    total_covered = 0
    total_missing = 0
    feature_rows: list[dict[str, Any]] = []

    for feat in data.get("features", []):
        f_cov = 0
        f_mis = 0
        for sf in feat.get("subfeatures", []):
            for tc in sf.get("tests", []):
                if tc.get("status") == "covered":
                    f_cov += 1
                else:
                    f_mis += 1
        total_covered += f_cov
        total_missing += f_mis
        f_total = f_cov + f_mis
        pct = round((f_cov / f_total) * 100, 1) if f_total else 0.0
        feature_rows.append(
            {
                "name": feat.get("name", "Unnamed Feature"),
                "covered": f_cov,
                "missing": f_mis,
                "total": f_total,
                "coverage_pct": pct,
            }
        )

    grand_total = total_covered + total_missing
    overall_pct = round((total_covered / grand_total) * 100, 1) if grand_total else 0.0
    return {
        "features_count": len(feature_rows),
        "covered": total_covered,
        "missing": total_missing,
        "total": grand_total,
        "coverage_pct": overall_pct,
        "by_feature": feature_rows,
    }


def build_mermaid(data: dict[str, Any], mode: str = "graph") -> str:
    """Generate Mermaid graph TD or mindmap syntax from the feature tree."""
    project = _mermaid_label(str(data.get("project", "Project")))
    if mode == "mindmap":
        lines = ["mindmap", f"  root(({project}))"]
        for feat in data.get("features", []):
            lines.append(f"    {_mermaid_label(feat.get('name', 'Feature'))}")
            for sf in feat.get("subfeatures", []):
                lines.append(f"      {_mermaid_label(sf.get('name', 'Sub-feature'))}")
                for tc in sf.get("tests", []):
                    tag = "PASS" if tc.get("status") == "covered" else "MISSING"
                    tid = tc.get("id", "TC")
                    title = _mermaid_label(tc.get("title", ""))
                    lines.append(f"        [{tag}] {tid}: {title}")
        return "\n".join(lines)

    lines = [
        "graph TD",
        "    classDef root fill:#1e293b,color:#f8fafc,stroke:#0f172a,stroke-width:2px;",
        "    classDef feature fill:#e0f2fe,color:#0c4a6e,stroke:#0284c7,stroke-width:2px;",
        "    classDef subfeature fill:#f1f5f9,color:#1e293b,stroke:#64748b,stroke-width:1px;",
        "    classDef covered fill:#dcfce7,color:#14532d,stroke:#16a34a,stroke-width:1px;",
        "    classDef missing fill:#ffedd5,color:#7c2d12,stroke:#ea580c,stroke-width:1px,stroke-dasharray: 4 3;",
        f'    ROOT["{project}"]:::root',
    ]

    for fi, feat in enumerate(data.get("features", []), start=1):
        fid = _safe_id(f"F_{feat.get('id', fi)}", f"F_{fi}")
        fname = _mermaid_label(feat.get("name", f"Feature {fi}"))
        lines.append(f'    ROOT --> {fid}["{fname}"]:::feature')

        for si, sf in enumerate(feat.get("subfeatures", []), start=1):
            sfid = _safe_id(f"SF_{fid}_{sf.get('id', si)}", f"SF_{fi}_{si}")
            sfname = _mermaid_label(sf.get("name", f"Sub-feature {si}"))
            lines.append(f'    {fid} --> {sfid}["{sfname}"]:::subfeature')

            for ti, tc in enumerate(sf.get("tests", []), start=1):
                tid_raw = str(tc.get("id", f"TC-{fi}-{si}-{ti}"))
                nid = _safe_id(f"T_{sfid}_{tid_raw}_{ti}", f"T_{fi}_{si}_{ti}")
                status = tc.get("status", "missing")
                cls = "covered" if status == "covered" else "missing"
                prefix = "OK" if status == "covered" else "GAP"
                t_type = str(tc.get("type", "unit")).upper()
                title = _mermaid_label(tc.get("title", ""))
                lines.append(f'    {sfid} --> {nid}["{prefix} {tid_raw} ({t_type}): {title}"]:::{cls}')

    return "\n".join(lines)


def build_html(data: dict[str, Any]) -> str:
    """Build a self-contained offline HTML tree viewer (zero external network calls)."""
    stats = compute_stats(data)
    project_esc = html.escape(str(data.get("project", "Project")))
    stack_esc = html.escape(str(data.get("stack", "")))
    # Escape closing script tags before embedding JSON inline.
    safe_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{project_esc} — Feature & Test Case Tree</title>
<style>
  :root {{
    --bg: #0f172a; --panel: #1e293b; --border: #334155; --text: #f1f5f9;
    --muted: #94a3b8; --accent: #38bdf8; --green: #22c55e; --green-bg: #14532d;
    --orange: #fb923c; --orange-bg: #7c2d12; --chip: #0f172a;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; }}
  header {{ padding: 20px 24px; border-bottom: 1px solid var(--border); background: var(--panel); }}
  h1 {{ margin: 0 0 4px; font-size: 1.35rem; }}
  .sub {{ color: var(--muted); font-size: 0.9rem; }}
  .wrap {{ max-width: 1120px; margin: 0 auto; padding: 20px 24px 48px; }}
  .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 18px; }}
  .kpi {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; }}
  .kpi .lbl {{ color: var(--muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; }}
  .kpi .val {{ font-size: 1.45rem; font-weight: 700; margin-top: 2px; }}
  .toolbar {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 18px; }}
  input, select, button {{ background: var(--panel); color: var(--text); border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; font-size: 0.9rem; }}
  input {{ flex: 1 1 240px; }}
  button {{ cursor: pointer; }}
  button:hover {{ border-color: var(--accent); }}
  .tree {{ display: flex; flex-direction: column; gap: 12px; }}
  details.feature {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 10px 14px; }}
  details.feature > summary {{ cursor: pointer; font-weight: 700; font-size: 1.02rem; display: flex; justify-content: space-between; align-items: center; }}
  details.subfeature {{ margin: 10px 0 6px 18px; padding-left: 14px; border-left: 2px solid var(--border); }}
  details.subfeature > summary {{ cursor: pointer; font-weight: 600; color: var(--accent); }}
  .src {{ color: var(--muted); font-size: 0.8rem; font-family: ui-monospace, monospace; margin-left: 8px; }}
  ul.tests {{ list-style: none; margin: 8px 0 4px 12px; padding: 0; display: flex; flex-direction: column; gap: 6px; }}
  li.tc {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; padding: 7px 10px; border-radius: 8px; background: var(--chip); border: 1px solid var(--border); font-size: 0.88rem; }}
  .badge {{ font-size: 0.72rem; font-weight: 700; padding: 2px 7px; border-radius: 999px; text-transform: uppercase; }}
  .covered {{ background: var(--green-bg); color: var(--green); border: 1px solid var(--green); }}
  .missing {{ background: var(--orange-bg); color: var(--orange); border: 1px solid var(--orange); }}
  .meta {{ color: var(--muted); font-size: 0.78rem; margin-left: auto; font-family: ui-monospace, monospace; }}
  .empty {{ color: var(--muted); text-align: center; padding: 32px; border: 1px dashed var(--border); border-radius: 10px; }}
</style>
</head>
<body>
<header>
  <h1>{project_esc} — Feature &amp; Test Case Tree</h1>
  <div class="sub">{stack_esc}</div>
</header>
<main class="wrap">
  <section class="kpis">
    <div class="kpi"><div class="lbl">Features</div><div class="val">{stats["features_count"]}</div></div>
    <div class="kpi"><div class="lbl">Total Cases</div><div class="val">{stats["total"]}</div></div>
    <div class="kpi"><div class="lbl">Covered</div><div class="val" style="color:var(--green)">{stats["covered"]}</div></div>
    <div class="kpi"><div class="lbl">Missing</div><div class="val" style="color:var(--orange)">{stats["missing"]}</div></div>
    <div class="kpi"><div class="lbl">Coverage</div><div class="val">{stats["coverage_pct"]}%</div></div>
  </section>
  <section class="toolbar">
    <input id="q" type="search" placeholder="Search feature, sub-feature, test ID, file..." />
    <select id="statusFilter">
      <option value="all">Status: All</option>
      <option value="covered">Covered only</option>
      <option value="missing">Missing only</option>
    </select>
    <select id="typeFilter">
      <option value="all">Type: All</option>
      <option value="unit">Unit</option>
      <option value="integration">Integration</option>
      <option value="e2e">E2E</option>
    </select>
    <button id="expandAll" type="button">Expand All</button>
    <button id="collapseAll" type="button">Collapse All</button>
  </section>
  <section id="tree" class="tree"></section>
</main>
<script>
const DATA = {safe_json};
const treeEl = document.getElementById("tree");
const qEl = document.getElementById("q");
const statusEl = document.getElementById("statusFilter");
const typeEl = document.getElementById("typeFilter");

function esc(s) {{
  return String(s ?? "").replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]));
}}

function render() {{
  const q = qEl.value.trim().toLowerCase();
  const st = statusEl.value;
  const tp = typeEl.value;
  const parts = [];

  for (const feat of (DATA.features || [])) {{
    const sfParts = [];
    let cov = 0, mis = 0;
    for (const sf of (feat.subfeatures || [])) {{
      const tcParts = [];
      for (const tc of (sf.tests || [])) {{
        const status = tc.status === "covered" ? "covered" : "missing";
        const type = (tc.type || "unit").toLowerCase();
        if (st !== "all" && status !== st) continue;
        if (tp !== "all" && type !== tp) continue;
        const hay = `${{feat.name}} ${{sf.name}} ${{sf.source_file || ""}} ${{tc.id}} ${{tc.title}} ${{tc.test_file || ""}}`.toLowerCase();
        if (q && !hay.includes(q)) continue;
        if (status === "covered") cov++; else mis++;
        const fileNote = tc.test_file ? esc(tc.test_file) : (tc.category ? `gap:${{esc(tc.category)}}` : "gap");
        tcParts.push(`<li class="tc"><span class="badge ${{status}}">${{status}}</span><strong>${{esc(tc.id)}}</strong><span>${{esc(tc.title)}}</span><span class="badge">${{esc(type)}}</span><span class="meta">${{fileNote}}</span></li>`);
      }}
      if (tcParts.length) {{
        const src = sf.source_file ? `<span class="src">${{esc(sf.source_file)}}</span>` : "";
        sfParts.push(`<details class="subfeature" open><summary>${{esc(sf.name)}}${{src}}</summary><ul class="tests">${{tcParts.join("")}}</ul></details>`);
      }}
    }}
    if (sfParts.length) {{
      parts.push(`<details class="feature" open><summary><span>${{esc(feat.name)}}</span><span class="sub">${{cov}} covered / ${{mis}} missing</span></summary>${{sfParts.join("")}}</details>`);
    }}
  }}

  treeEl.innerHTML = parts.length ? parts.join("") : '<div class="empty">No matching test cases.</div>';
}}

qEl.addEventListener("input", render);
statusEl.addEventListener("change", render);
typeEl.addEventListener("change", render);
document.getElementById("expandAll").addEventListener("click", () => treeEl.querySelectorAll("details").forEach(d => d.open = true));
document.getElementById("collapseAll").addEventListener("click", () => treeEl.querySelectorAll("details").forEach(d => d.open = false));
render();
</script>
</body>
</html>
"""


def _run_self_test() -> None:
    sample = {
        "project": 'Demo [v1] "Core"',
        "stack": "Python",
        "features": [
            {
                "id": "F-1",
                "name": "Auth [Login]",
                "subfeatures": [
                    {
                        "id": "SF-1",
                        "name": "Token",
                        "source_file": "src/auth.py",
                        "tests": [
                            {"id": "TC-1", "title": "Valid login", "status": "covered", "type": "unit", "category": "happy", "test_file": "tests/test_auth.py"},
                            {"id": "TC-2", "title": 'Expired "token" rejected</script>', "status": "missing", "type": "integration", "category": "error", "test_file": ""},
                        ],
                    }
                ],
            }
        ],
    }
    stats = compute_stats(sample)
    assert stats["covered"] == 1 and stats["missing"] == 1 and stats["coverage_pct"] == 50.0
    mmd = build_mermaid(sample, mode="graph")
    assert "graph TD" in mmd and '["Demo (v1) \'Core\'"]:::root' in mmd
    assert "mindmap" in build_mermaid(sample, mode="mindmap")
    html_out = build_html(sample)
    assert "http://" not in html_out and "https://" not in html_out
    assert "<\\/script>" in html_out
    print("Self-test passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Feature & Test Case Tree to Mermaid and offline HTML.")
    parser.add_argument("input", nargs="?", type=Path, help="Path to feature-test-tree JSON file")
    parser.add_argument("--html-out", type=Path, default=None, help="Output path for interactive HTML file")
    parser.add_argument("--md-out", type=Path, default=None, help="Output path for Mermaid markdown file")
    parser.add_argument("--mermaid-mode", choices=["graph", "mindmap"], default="graph", help="Mermaid diagram style")
    parser.add_argument("--self-test", action="store_true", help="Run built-in verification checks and exit")
    args = parser.parse_args()

    if args.self_test:
        _run_self_test()
        return

    if not args.input or not args.input.exists():
        parser.error("Provide an existing JSON file path (or run --self-test).")

    data = json.loads(args.input.read_text(encoding="utf-8"))
    mermaid = build_mermaid(data, mode=args.mermaid_mode)
    stats = compute_stats(data)

    if args.md_out:
        args.md_out.write_text(f"```mermaid\n{mermaid}\n```\n", encoding="utf-8")
    if args.html_out:
        args.html_out.write_text(build_html(data), encoding="utf-8")

    print(json.dumps({"stats": stats, "mermaid": mermaid}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
