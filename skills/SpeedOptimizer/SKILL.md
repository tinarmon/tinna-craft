---
name: SpeedOptimizer
description: Full-stack performance planning and acceleration engine for Python backends & data pipelines, Web frontends, Local AI inference (quantization, VRAM, batching), and Vector/SQL databases. Enforces profiling (cProfile, tracemalloc), anti-pattern audits (vectorization, downcasting, chunking), interactive hybrid planning, user trade-off selection, and benchmarked execution.
triggers: SpeedOptimizer, optimize speed, boost performance, cprofile, vectorization, เปิดโหมด optimize, เพิ่มความเร็วโค้ด
---

# SpeedOptimizer: Software, Web, Data & Local AI Performance Engine

When this skill is activated (e.g., user says *"optimize it"*, *"speed up"*, *"เปิดโหมด optimize"*, *"boost performance"*, *"make it faster"*, *"perf-optimizer"*, or *"use SpeedOptimizer"*), **you MUST strictly follow the 4-Phase Performance Engineering Protocol below** on EVERY turn for the remainder of this session until explicitly deactivated.

---

## 1. Lifecycle & State Management

- **Status:** **ACTIVE** once invoked or enabled.
- **Duration:** Persists across all subsequent user requests in the session.
- **Deactivation:** Only disable these constraints if the user explicitly says:
  `"stop optimize"`, `"ปิดโหมด optimize"`, `"disable SpeedOptimizer"`, or `"exit optimize"`.
- **Deactivation Output:** `[SpeedOptimizer deactivated. Returned to standard development mode.]`

---

## 2. The 4-Phase Optimization Protocol (Never Skip Planning)

```mermaid
flowchart LR
    A["Phase 1: Profile & Diagnostic"] --> B["Phase 2: Hybrid Interactive Plan"]
    B --> C["Phase 3: User Trade-off Decision"]
    C --> D["Phase 4: Execution & Benchmark"]
```

### Phase 1: Deep Profiling & Root-Cause Diagnosis
Never guess bottlenecks or apply blind refactors. Always measure baseline before and after changes.

1. **Wall-Time & Function Profiling:**
   - Python: Targeted timing with `time.perf_counter()`.
   - Function-level bottleneck profiling with `cProfile`:
     ```powershell
     python -m cProfile -s cumulative script.py
     ```
2. **Memory Footprint & Allocation Tracing:**
   - Inspect DataFrame memory: `df.info(memory_usage="deep")`
   - Trace RAM allocation with standard library `tracemalloc`:
     ```python
     import tracemalloc
     tracemalloc.start()
     # code ...
     current, peak = tracemalloc.get_traced_memory()
     print(f"Peak memory: {peak / 10**6:.2f} MB")
     tracemalloc.stop()
     ```
3. **Bottleneck Categorization:**
   - **Compute Bound:** Loops, unvectorized math, synchronous blocking.
   - **Memory / VRAM Bound:** Large model footprints, memory leaks, uncompressed data types, lacking streaming.
   - **I/O & Network Bound:** Slow queries, N+1 patterns, unindexed tables, non-async calls.
   - **Frontend / Rendering:** Oversized bundles, excessive re-renders, main-thread blocking.

---

### Phase 2 & 3: Hybrid Interactive Planning (Plan Artifact + User Choice)
Before making intrusive code modifications:

1. **Create a Performance Plan Artifact** (`performance_plan.md`) summarizing:
   - **Current Baseline / Bottleneck Analysis:** What is slowing things down and why.
   - **Proposed Optimization Tiers:**
     - **Tier 1 (Safe / Quick Wins):** Zero-risk optimizations (vectorization, caching, query indexing, async conversions, asset minification).
     - **Tier 2 (Architectural / Algorithmic):** Restructuring data pipelines, batching, chunking, multiprocessing, Web Worker offload.
     - **Tier 3 (Aggressive / High-Impact Trade-offs):** Model quantization (FP16 -> INT8/INT4/GGUF), lossy compression, architectural re-write.
   - **Estimated Performance Gain & Trade-offs:** Latency vs. RAM/VRAM vs. Accuracy/Quality.

2. **Present Choices to the User**:
   - Ask the user which optimization tiers or specific strategies they want to prioritize before executing changes.

---

### Phase 4: Domain-Specific Execution & Best Practices

#### A. Python & Data Pipeline Performance (Pandas, Polars, NumPy)
1. **Ban Iterative Row Loops:**
   - **Strictly Avoid:** `for index, row in df.iterrows():`, `.itertuples()`, or slow `.apply(axis=1)` where vectorized logic exists.
   - **Replace With:**
     - Native vectorized series operations: `df["total"] = df["qty"] * df["price"]`
     - NumPy boolean indexing: `np.where(condition, x, y)`
     - Dictionary mapping: `df["category"] = df["code"].map(mapping_dict)`
2. **High-Performance GroupBy & Aggregations:**
   - Filter rows *before* grouping, not after.
   - Compute only needed columns: `df.groupby("dept")["salary"].mean()` instead of `df.groupby("dept").mean()["salary"]`.
3. **Memory Optimization & Type Downcasting (Cut RAM 50–80%):**
   - **Numeric Downcasting:**
     ```python
     df["int_col"] = pd.to_numeric(df["int_col"], downcast="integer")
     df["float_col"] = pd.to_numeric(df["float_col"], downcast="float")
     ```
   - **Categorical Types:** Convert repeated low-cardinality strings to `category`:
     ```python
     df["status"] = df["status"].astype("category")
     ```
   - **Explicit Garbage Collection:**
     ```python
     del raw_data
     import gc; gc.collect()
     ```
4. **Chunking & Streaming for Large Datasets:**
   - Never load multi-gigabyte files entirely at once:
     ```python
     for chunk in pd.read_csv("large_file.csv", chunksize=50_000):
         process(chunk)
     ```
   - Use Python generators (`yield`) rather than accumulating large lists in memory.

#### B. Local AI & Model Inference Optimization
- **Quantization:** Convert FP32/FP16 models to GGUF (Q4_K_M, Q5_K_M), AWQ, or INT8/INT4.
- **Inference Engines:** Leverage `onnxruntime-gpu`, TensorRT, `vLLM` PagedAttention, or `llama.cpp` AVX/GPU offloading.
- **KV Cache & Flash Attention:** Limit context window bloating, enable PyTorch SDPA (`torch.nn.functional.scaled_dot_product_attention`) and prompt caching.
- **Vectorized Batching:** Process embeddings and inference calls in batches rather than 1-by-1 loops.

#### C. Backend & API Optimization (FastAPI, AsyncIO)
- **Non-blocking I/O:** Convert blocking database/file/network calls to `asyncio` (`aiohttp`, `httpx`, `asyncpg`, `motor`).
- **Multiprocessing vs Threading:** Use `ProcessPoolExecutor` for CPU-heavy AI preprocessing; `ThreadPoolExecutor` for I/O tasks.
- **Layered Caching:** Fast in-memory (`lru_cache`, `cachetools`) or disk caching (`diskcache`) for expensive compute/embeddings.
- **Zero-Copy Streaming:** Use `StreamingResponse` for large AI outputs and file transfers.

#### D. Web Frontend & UI Performance (React, Next.js, Vue)
- **Bundle & Asset Splitting:** Dynamic imports (`React.lazy()`, code splitting), tree-shaking, and WebP/AVIF asset compression.
- **Render Optimization:** Debounce user input, memoize expensive calculations (`useMemo`, `useCallback`), virtualize large lists (chat transcripts).
- **Web Workers:** Offload local browser AI processing (Transformers.js, WebLLM) to background Web Workers.
- **Core Web Vitals:** Minimize LCP, CLS, and INP.

#### E. Database & Vector Store Optimization (SQL, ChromaDB, FAISS)
- **Vector Index Tuning:** Tune HNSW parameters (`M`, `efConstruction`, `efSearch`) for search recall vs. query latency.
- **SQL & ORM Hardening:** Add proper composite indexes, avoid `SELECT *`, eliminate N+1 queries using `select_related`/`joinedload`, use connection pools.
- **Batch Upserts:** Always batch vector embeddings and database writes.

---

## 3. Post-Optimization Evidence Card

Always conclude performance optimization with an evidence card:
```
## Performance Optimization Report
⚡ Execution Time: <Before>s -> <After>s (<X>x speedup)
💾 Peak Memory: <Before>MB -> <After>MB (<Y>% reduction)
🔧 Key Changes: <e.g., replaced iterrows with vectorized np.where, downcasted float64 to float32, added index>
✅ Integrity: 100% test pass / zero data corruption
```

---

## 4. Immediate Confirmation on Activation

When this skill is first read/activated, output this confirmation line:
`⚡ [SpeedOptimizer Active] Full-stack & data performance planning, deep profiling & multi-stack speed engine enabled. (Type 'stop optimize' to disable)`
