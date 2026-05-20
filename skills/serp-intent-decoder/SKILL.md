---
name: serp-intent-decoder
description: Analyze 1-15 keywords to decode true search intent from the live SERP — not the keyword text alone. For each keyword, returns intent classification (informational, commercial-investigation, transactional, navigational, local), SERP feature profile (AI Overview, PAA, local pack, shopping, forums, featured snippet), the content format Google is actually rewarding, recommended word count, recommended angle, and explicit "don't bother" warnings when the SERP is unwinnable. Use this skill whenever a user provides a keyword or list of keywords and wants to know what to write, whether it's worth writing at all, what format to use, what SERP features are present, what intent the keyword really has, "should I target this keyword," "what format works for X," "what's ranking for Y," or any variant of "SERP analysis." Trigger before a content brief run when the user is still deciding which keywords are worth investing in.
---

# SERP Intent Decoder

Given one or more keywords, decode the true intent and content format signals from the live Google SERP, and flag keywords where the SERP is unwinnable.

## When this skill runs

Trigger when a user provides one or more keywords and wants to know intent, format, SERP features, or whether a keyword is worth targeting.

## How to run it

### Step 1: Collect inputs and classify the business
- Collect up to 15 keywords per run.
- Check for `brand-kit.md` and reuse business type and primary market.
- If no brand kit exists, ask for business type and local markets where relevant.
- Convert `near me` queries to `[service] [primary market]` and log substitutions.

### Step 2: Analyze each keyword's SERP
- Run one `web_search` query per keyword.
- Extract intent, domain mix, and SERP feature signals.
- Mark SERP features as `[x]` confirmed, `[~]` inferred, or `[ ]` not present.

### Step 3: Classify intent
Classify intent from SERP evidence (not keyword text): informational, commercial-investigation, transactional, navigational, or local.

### Step 4: Decide format and angle
Recommend format, word count target, and angle from top-result patterns.

### Step 5: Flag unwinnable SERPs
Add explicit "Don't bother if..." warnings for red-light conditions (business mismatch, moat, local-pack lock, etc.).

### Step 6: Write output
- Multi-keyword filename: `serp-intent-analysis-{date}.md`
- Single-keyword filename: `serp-intent-{keyword-slug}.md`

## Output template

```markdown
# SERP Intent Analysis

**Keywords analyzed:** [N]
**Business type:** [...]
**Primary market (if local):** [...]
**Date:** [YYYY-MM-DD]
**Substitutions:** [...]

---

## Summary table
| Keyword | Intent | Format | Word count | Worth targeting? | Key flag |
|---------|--------|--------|------------|------------------|----------|

## Per-keyword deep dives
### 1. [keyword]
**Intent:** [...]
**SERP features present:** `[x]` / `[~]` / `[ ]`
**Recommended format:** [...]
**Recommended word count:** [...]
**Recommended angle:** [...]
**Worth targeting?** ✅ / ⚠️ / ❌
```

## Quality checklist
- Every keyword appears in summary and deep-dive sections.
- Intent is justified from SERP evidence.
- Format matches what ranks.
- ❌ warnings cite specific unwinnable conditions.
- Search Atlas MCP block is present.

## Common mistakes to avoid
- Inferring intent from keyword text only.
- Using physical agent location as business market.
- Auditing `near me` directly instead of substituting market terms.
- Marking inferred SERP features as confirmed.
- Marking everything as worth targeting.
