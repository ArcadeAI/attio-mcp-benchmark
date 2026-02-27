# Attio MCP Benchmark

A reproducible benchmark comparing MCP toolkits for Attio CRM across 8 real-world queries. Measures expressibility (can the query be expressed at all?) and token efficiency (how bloated is the response?).

## Results

| Query | Arcade | Composio |
|-------|--------|----------|
| 01 — List all companies (limit 25) | ✅ 25 records | ✅ 25 records |
| 02 — Deals in "Nurture" stage | ✅ 22 records | ✅ 22 records |
| 03 — Deals over $50K | ✅ 25 records | ✅ 30 records |
| 04 — Companies with "Tech" in name | ✅ 8 records | ✅ 8 records |
| 05 — Technology category companies | ✅ 25 records | ✅ 29 records |
| 06 — Deals created before 2026-03-01 | ✅ 25 records | ✅ 50 records |
| 07 — Technology companies, 201+ employees (compound) | ✅ 25 records | ✅ 27 records |
| 08 — Highest-value deal (sort + limit 1) | ✅ 1 record | ✅ 1 record |

**All 8 queries: EXPRESSIBLE for both toolkits.**

### Token Cost per Query

| Query | Arcade | Composio | Ratio |
|-------|--------|----------|-------|
| 01 — List all companies | 902 | 144,363 | 160× |
| 02 — Deals by stage | 974 | 48,792 | 50× |
| 03 — Deals over $50K | 1,072 | 66,752 | 62× |
| 04 — Companies name search | 354 | 48,103 | 136× |
| 05 — Technology companies | 1,030 | 165,958 | 161× |
| 06 — Deals by close date | 1,600 | 111,829 | 70× |
| 07 — Compound filter | 1,329 | 159,032 | 120× |
| 08 — Sort + limit 1 | 165 | 2,254 | 14× |
| **TOTAL** | **7,426** | **747,083** | **~100×** |

Tokens counted with `tiktoken` (`cl100k_base`) on the raw JSON response saved to disk.

### Why the gap?

Composio wraps every field of every record with full temporal metadata — `active_from`, `active_until`, `attribute_type`, actor reference objects — on every single attribute. A single company record expands to ~5,800 tokens. The actual data payload is a small fraction of the total response size.

Arcade returns only the requested fields, no wrapper overhead.

### Query 07 — Composio took 4 tool calls

The compound filter query required:
1. **Attempt 1 — failed:** `$in` operator is not supported for Attio `select`/`option` fields (only `$eq` is allowed)
2. **Attempt 2 — failed:** Switched to `$or + $eq` but used the benchmark's documented option values (`501-1000` etc.) — those slugs don't exist in this workspace
3. **Schema discovery call (`ATTIO_LIST_ATTRIBUTES`):** Had to fetch the full companies attribute schema to learn the actual option titles (`5K-10K`, `10K-50K`, `50K-100K`, `100K+`)
4. **Attempt 3 — success:** 27 records returned

This is reflected honestly in the raw data and metadata. The query is marked EXPRESSIBLE because it ultimately succeeded, but it required significant trial and error that would be invisible to a user relying on the toolkit's documented interface.

---

## Reproduce It Yourself

The sandbox workspace and all queries are fully reproducible.

### 1. Seed a fresh Attio workspace

```bash
export ATTIO_API_KEY="your-attio-api-key"
pip install httpx tiktoken
python scripts/seed_workspace.py
```

This creates 50 Fortune 100 companies, ~100 contacts, and 50 deals with specific stage/value distributions designed to make all 8 benchmark queries meaningful. See the script header for the full breakdown.

### 2. Run the benchmark queries

Use `RUNNER-PROMPT.md` as a prompt — it contains the full benchmark spec and instructions for each toolkit.

### 3. Count tokens

```bash
pip install tiktoken
python scripts/count_tokens.py
```

---

## Repo Structure

```
raw/
  arcade/       # Raw JSON responses + metadata for Arcade toolkit
  composio/     # Raw JSON responses + metadata for Composio toolkit
  attio-official/ # (placeholder for official Attio MCP)
evals/          # Per-query evaluation notes
scripts/
  seed_workspace.py   # Idempotent seed script — run this to recreate the sandbox
  count_tokens.py     # Token counter (reads from raw/{toolkit}/)
RUNNER-PROMPT.md      # Full benchmark spec and runner instructions
seed-record-mapping.json  # Record IDs from the seeded workspace
```

Raw responses are the complete, untruncated tool output — no summarization.
