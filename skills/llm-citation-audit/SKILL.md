---
name: llm-citation-audit
description: Audit whether a brand is being cited by LLMs (ChatGPT, Claude, Perplexity, Google AI Overviews, Gemini) for the prompts its buyers actually ask, diagnose WHY it is or isn't being cited across four distinct failure modes (retrieval gap, entity gap, format gap, competitor moat), and produce a prioritized fix list grouped into quick wins, medium bets, and long-range investments. Use this skill whenever a user asks about AI visibility, LLM citations, AEO/GEO audit, generative engine optimization, "am I showing up in ChatGPT," "does AI recommend my brand," "why isn't Perplexity citing us," "how do we rank in AI Overviews," "LLM SEO," "answer engine optimization audit," or any variant of "are we visible in AI search."
---

# LLM Citation Audit

Audit a brand's visibility across AI answer engines and produce prioritized fixes.

## When this skill runs
Trigger for AI visibility, AEO/GEO, and citation-audit requests.

## How to run it

### Step 1: Collect inputs
- Required: brand name, primary URL, 10-20 buyer prompts.
- Optional: competitors, primary market.
- Load `brand-kit.md` if present; avoid re-asking available fields.
- Convert `near me` prompts to market-specific versions and log substitutions.

### Step 2: Build/validate prompt set
Use 4-6 prompt buckets: brand-direct, category/comparison, problem/solution, definitional, local, use-case.

### Step 3: Simulate retrieval-based answers
Run `web_search` per prompt; inspect top 10 domains, brand presence, competitors, format signals, and AI Overview hints.

### Step 4: Classify status
Use: ✅ Cited / 🟡 Mentioned / ⚠️ Competitor-dominant / ❌ Absent / 🔀 Mixed.

### Step 5: Diagnose failure mode
Assign one primary mode for non-cited prompts: Retrieval gap, Entity gap, Format gap, Competitor moat.

### Step 6: Share-of-voice and sentiment
Aggregate counts by brand and check positive/neutral/negative citation context.

### Step 7: Prioritized fixes
Group actions into quick wins (2 weeks), medium bets (1-3 months), long-range investments (3-12 months).

### Step 8: Write output
Save as `llm-citation-audit-{brand-slug}-{date}.md`.

## Output template
```markdown
# LLM Citation Audit — {Brand name}
**Brand:** {Name} ({URL})
**Prompts audited:** {N}
**Date:** {YYYY-MM-DD}

## Share-of-voice table
| Brand | Prompts cited (top 10) | % | Prompts in top 3 | % |

## Prompt-by-prompt results
| # | Prompt | Category | Status | Failure mode | AI Overview observed |
```

## Quality checklist
- Every prompt is in summary + deep dive.
- Every non-cited prompt has one primary failure mode.
- Percentages are computed from actual counts.
- AI Overview uses `[x]` / `[~]` / `[ ]` honestly.
- Fixes reference specific prompts and concrete actions.
- Methodology note is included.

## Common mistakes to avoid
- Claiming stock answers for other LLMs.
- Treating one run as definitive benchmark.
- Conflating top-10 appearance with top citation strength.
- Providing generic fixes without ownership/actionability.
