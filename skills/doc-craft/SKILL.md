---
name: doc-craft
description: >-
  Use this skill when creating, formatting, editing, or reviewing any document,
  report, proposal, executive summary, .docx, .pdf, .pptx, Markdown, README,
  CLI usage runbook, or Architecture Decision Record (ADR). Enforces
  Anti-AI-Slop editorial writing (TH/EN BLUF prose, banned clichés),
  Thai/International typography, editorial Booktabs tables, Print-CSS PDF
  pipelines, reality-synced code docs, and `0N_{ชื่อเอกสาร}` sequential
  versioning. Triggers on "เขียนเอกสาร", "จัดหน้าเอกสาร", "ทำรายงาน",
  "ไม่เอา AI slop", "write doc", "format report", or ADR/README updates.
triggers: doc-craft, write doc, format report, anti-ai-slop, เขียนเอกสาร, จัดหน้าเอกสาร, ทำรายงาน, ไม่เอา AI slop, 0N_
---

# Doc Craft: Reality-Synced Documentation & Decision Records

Ensures documentation is clear, accurate, and kept in sync with actual code and data behavior.

---

## Part 1: Reality-Synced Documentation & Runbooks

Never document theoretical code. Documentation must match executable reality.

### 1. Ground Truth Verification
- Before writing a command example, verify it runs (`python script.py --help` or run on sample input).
- Ensure all mentioned file paths, function signatures, and parameter flags actually exist in the codebase.
- Avoid broken links or placeholder copy (`TODO`, `<your-api-key-here>` without explanation).

### 2. Standard Runbook / README Structure
When documenting a tool, script, or pipeline, include:
1. **Overview & Purpose:** 1–2 sentences explaining what problem this script solves and who uses it.
2. **Prerequisites & Dependencies:** Required Python version and packages (e.g., `pip install -r requirements.txt`).
3. **Usage Examples:** Concrete, copy-pasteable terminal commands for common use cases:
   ```bash
   python process_data.py --input raw/data.csv --output cleaned/data.parquet
   ```
4. **Parameters Table:**
   | Flag / Option | Type | Default | Description |
   |---|---|---|---|
   | `--input`, `-i` | Path | *Required* | Path to input source file |
   | `--output`, `-o`| Path | `output.csv` | Destination path for processed data |
   | `--verbose` | Flag | `False` | Enable debug logging output |
5. **Expected Output:** Description of the generated files, schemas, or exit codes.
6. **Troubleshooting / FAQ:** 2–3 common error scenarios and how to resolve them.

---

## Part 2: Architecture Decision Record (ADR)

When making non-trivial technical or architectural decisions (e.g., choosing Polars vs Pandas, selecting SQLite vs JSON, restructuring pipeline storage):

Document the decision in `docs/decisions/<YYYY-MM-DD>-<decision-slug>.md` using this format:

```markdown
# ADR: [Decision Title]

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Deprecated
- **Context:** [What problem or requirement triggered this choice?]

## Considered Options
1. **Option A:** [Description]
2. **Option B:** [Description]

## Trade-off Analysis
| Criteria | Option A | Option B |
|---|---|---|
| Performance / Scalability | ... | ... |
| Complexity / Maintenance | ... | ... |
| Dependencies | ... | ... |

## Decision & Rationale
We chose **[Option X]** because [key reasons, e.g., zero external dependencies, native speed].

## Consequences
- **Positive:** [What do we gain?]
- **Negative / Risks:** [What limitations or trade-offs must we accept?]
```

---

## Part 3: Document & PDF Sequential Versioning Standard

When generating, exporting, renaming, or managing documents (`.docx`, `.pdf`, `.pptx`, `.xlsx`, `.md` reports), **always enforce sequential versioning with a zero-padded prefix** so file explorers sort them chronologically from oldest to newest:

### 1. The Standard Format: `0N_{ชื่อเอกสาร}`
- **Format:** `0N_{Document_Name}.{ext}`
- **Zero-Padding Rule:**
  - 1–99 versions: Use 2 digits (`01`, `02`, `03`, ... `09`, `10`, `11`, ... `N`)
  - 100+ versions: Use 3 digits (`001`, `002`, ... `100`)
- **Ordering Principle (เก่า -> ใหม่):**
  - `01_{ชื่อเอกสาร}` = ฉบับร่างแรกสุด / ต้นฉบับเริ่มต้น (Initial Draft)
  - `02_{ชื่อเอกสาร}` = ฉบับแก้ไขรอบถัดมา
  - `0N_{ชื่อเอกสาร}` = ฉบับล่าสุด / ฉบับสมบูรณ์

### 2. Examples
```text
docs/
├── 01_โครงร่างงานวิจัย_ฉบับร่าง.docx
├── 02_โครงร่างงานวิจัย_แก้ไขตามผู้ทรงคุณวุฒิ.docx
├── 03_โครงร่างงานวิจัย_ฉบับสมบูรณ์.docx
└── 03_โครงร่างงานวิจัย_ฉบับสมบูรณ์.pdf
```

### 3. Anti-Patterns to Eliminate
- **Ban chaotic suffixes:** Never name files `report_final.docx`, `report_final2.docx`, `report_really_final.pdf`, or `report_edit_new.docx`.
- **Always update the sequence number:** When a document is modified or re-exported with substantive changes, advance the prefix: `01_...` -> `02_...`.
- **Preserve Archive History:** When keeping history, do not delete older versions unless asked; their `01_`, `02_` prefixes keep the full audit trail sorted automatically.

---

## Part 4: Anti-AI-Slop Editorial & Copywriting Rules (TH / EN)

Apply these editorial rules across all reports, proposals, executive summaries, READMEs, and Notion/Word/PDF deliverables so documents read as authored by an experienced practitioner rather than generated by an LLM.

### 1. BLUF (Bottom Line Up Front) Structure
- Open every document and major section with the core conclusion, decision, recommendation, or concrete numbers within the **first 1–2 sentences**.
- Ban throat-clearing introductions that restate obvious background before reaching the point.
- Ban repetitive closing summaries that merely echo preceding bullets (*"กล่าวโดยสรุปคือ..."*, *"In conclusion..."*, *"To summarize..."*). End on the final substantive action item, decision, or next step.

### 2. Banned AI Clichés & Translationese
Eliminate stock LLM vocabulary and stiff translated phrasing:
- **Thai Banned Phrases:**
  - *"ในยุคดิจิทัลที่เปลี่ยนแปลงอย่างรวดเร็ว"*, *"ในปัจจุบันที่..."* (when used as empty filler)
  - *"มีบทบาทสำคัญอย่างยิ่ง"*, *"ถือเป็นก้าวสำคัญ"*, *"ยกระดับสู่..."*, *"ตอบโจทย์อย่างแท้จริง"*
  - *"ไม่เพียงแต่... แต่ยัง..."* (when used formulaically across sections)
  - *"เปรียบเสมือนดาบสองคม"*, *"กล่าวโดยสรุปคือ"*, *"ท้ายที่สุดนี้"*
  - Unnatural translationese passive voice (*"ถูกทำให้..."*, *"ได้รับการออกแบบมาเพื่อ..."*, *"มันเป็นสิ่งสำคัญที่จะ..."*) where direct Thai active voice is clearer.
- **English Banned Words & Phrases:**
  - *delve, testament, tapestry, crucial, pivotal, landscape, underscore, foster, seamless, cutting-edge, game-changer, leverage* (as vague buzzword), *robust* (without metrics).
  - *"In today's fast-paced world"*, *"It is important to note that"*, *"Not only... but also..."*, *"Whether you're X or Y..."*.

### 3. Structural Anti-Patterns to Eliminate
- **Ban Wall of `**Bold:**` Bullets:** Never format every paragraph as a bullet list of `**Topic:** explanation`. Write cohesive prose paragraphs for narrative, context, and trade-offs; reserve bullets for true discrete lists (3–6 items) and use a structured table when comparing multiple attributes.
- **Punctuation & Emoji Discipline:** Ban decorative emojis (`🚀`, `✨`, `💡`, `✅`, `📌`) in formal documents, executive reports, specs, and technical READMEs unless explicitly requested by the user. Avoid AI-style overuse of em-dashes (`—`); use natural Thai spacing, conjunctions, commas, or parentheses instead.
- **Concrete Metrics over Vague Claims:** Replace empty qualifiers (*"เร็วขึ้นมาก"*, *"เพิ่มประสิทธิภาพสูง"*, *"significantly faster"*) with measured figures, ranges, counts, or specific mechanisms.

---

## Part 5: Thai & International Document Typography & Layout Spec (`.docx`, `.pdf`, Markdown)

### 1. Font Pairing & Thai Script Calibration
- **Thai Official / Academic / Government:** Use `TH Sarabun New` (16 pt body / 18–20 pt headings) or `Sarabun` (11–12 pt body).
- **Modern Executive / Tech Reports (TH + EN):** Use `IBM Plex Sans Thai`, `Anuphan`, or `Noto Sans Thai` paired with `Inter` or `IBM Plex Sans` for Latin text/numbers, and `JetBrains Mono` or `Consolas` for code and identifiers.
- **Zero Uncalibrated Latin Defaults:** Never leave Thai text on default `Arial`, `Calibri`, or `Times New Roman`, which lack proper Thai glyph metrics and cause floating/overlapping vowels and tone marks (สระลอย / วรรณยุกต์ทับ).
- **Line Height & Paragraph Spacing:** Enforce `1.35–1.5` line height in CSS/PDF or `Multiple 1.15–1.25` in `.docx`, with explicit paragraph spacing (`Before: 0–4pt`, `After: 6–8pt`) so Thai upper/lower vowels never collide across lines. Never insert empty spacer paragraphs or double blank lines for vertical rhythm.
- **Alignment & Thai Word Wrapping:** Use `Left` alignment for modern executive and technical reports, or `thaiDistribute` for formal Thai official documents with clean word boundaries. Never use standard Latin `Justify` on narrow Thai columns, which stretches inter-word gaps awkwardly.

### 2. Editorial Tables (Booktabs Style — Ban Boxy Black Grids)
- **Ban Default Grid Borders:** Never apply heavy 4-sided black borders (`SOLID` black boxes) around every cell.
- **Booktabs / Editorial Rules:** Apply a clean top rule and header bottom rule (`1pt–1.5pt` slate/dark gray `#334155`), subtle horizontal row dividers (`0.5pt` `#E2E8F0`) or light alternating row shading (`#F8FAFC`), and **no vertical borders**.
- **Cell Alignment & Padding:**
  - Left-align text and label columns.
  - **Right-align all numeric, currency, and percentage columns** with consistent decimal precision.
  - Center short fixed-width codes, status tags, or ISO dates.
  - Enforce comfortable cell padding (`6–8pt` vertical, `8–10pt` horizontal) so text never touches rule lines.

### 3. Page Flow & Hierarchy Control
- **No Orphaned Headings:** Always enable `keepNext` (`keep_with_next` in Word / `break-after: avoid` in CSS) on every heading level so no heading appears stranded at the bottom of a page.
- **Table Continuity:** Enable repeating table headers across page breaks (`tblHeader` in `.docx` / `<thead>` in HTML) and prevent mid-row page splits (`cantSplit` / `break-inside: avoid` on `tr`).
- **Restrained 3-Level Hierarchy:** Restrict headings to `H1`, `H2`, and `H3`, differentiated strictly by font scale, weight, and spacing—never by gaudy rainbow accent colors or excessive underlines.

---

## Part 6: High-Craft PDF Pipeline & Mandatory Visual QA

### 1. Prefer Print-CSS (HTML -> PDF) or Typst over Raw ReportLab
- For newly designed multi-page reports, executive briefs, or proposals exported to PDF, generate semantic HTML + `@page` / `@media print` CSS (rendered via Playwright/headless Chromium) or `typst` instead of low-level `reportlab` canvas coordinates.
- Print-CSS and Typst provide native HarfBuzz/browser Thai word breaking, exact glyph shaping (zero floating tone marks), CSS Grid/Flexbox layouts, crisp SVG diagrams, and predictable pagination. Reserve `pypdf` / `pdfplumber` for merging, splitting, form filling, or extraction tasks.

### 2. Visual Verification Gate
Before declaring any generated `.docx` or `.pdf` deliverable complete, convert/render pages to inspect visually (or inspect PDF page renders) and verify all four checks:
1. **Thai Script Integrity:** Zero clipped, overlapping, or floating vowels/tone marks across body text, headings, and table cells.
2. **Pagination Integrity:** Zero orphaned headings at page bottoms and zero awkwardly split table rows.
3. **Table & Margin Discipline:** Zero overflowing columns, boxy black grid borders, or unaligned numeric columns.
4. **Editorial Cleanliness:** Zero AI-slop clichés, zero `**Bold:**` bullet walls, and zero unauthorized decorative emojis.

