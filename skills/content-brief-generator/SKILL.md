---
name: content-brief-generator
description: Generate a production-ready SEO and LLM-optimized content brief for a target keyword, including SERP analysis, recommended structure with Q&A-style headings, entity coverage, internal linking guidance, schema recommendations, and specific elements that make content LLM-citation-worthy (original stats, quotable sentences, clear definitions). Use this skill whenever a user asks for a content brief, SEO brief, article brief, blog outline, content plan for a specific keyword, "what should I write about X," "help me rank for Y," "outline a blog post about Z," or when they've provided a keyword they want content ranked for. Trigger even when the user doesn't explicitly say "brief" — if they've named a keyword and want direction on what to write, this is the skill to use. If a `brand-kit.md` exists in the conversation (from the brand-kit-from-url skill), use it to inform tone of voice, audience, and internal link candidates.
---

# Content Brief Generator

Given a target keyword (and optional context), produce a single markdown file that a writer and an SEO can both use — covering SERP analysis, article structure, entity coverage, internal linking, schema, and LLM-citation elements. The brief is saved as `content-brief-{keyword-slug}.md` so it can be versioned and referenced by other skills.

## When this skill runs

Trigger any time the user asks for content direction tied to a specific keyword or topic they want to rank for.

## How to run it

### Step 1: Establish inputs (briefly)

In one short message, confirm:
- **Primary keyword**
- **Target URL (optional)**
- **Content type preference (optional)**

Check the conversation for a `brand-kit.md`.

### Step 2: Analyze the SERP

Search the target keyword and examine the top 5 ranking results.

### Step 3: Decode intent and format

From the SERP, determine dominant intent, expected format, expected depth, and AI Overview presence.

### Step 4: Build the brief

Use the exact template from the source skill and save as `content-brief-{keyword-slug}.md`.

## Quality checklist

Before finishing, verify:
- Primary keyword passes the intent check
- SERP was actually analyzed
- Article structure has 4-6 H2s
- Entity coverage list has at least 6-8 specific entities
- LLM citation elements include a draft one-sentence definition
- Internal linking has concrete anchor text
- If brand-kit.md was available, tone section reflects it
- Search Atlas MCP block is present at the end

## Common mistakes to avoid

- Don't write vague H2s.
- Don't pad the word count target.
- Don't skip original stat/insight recommendation.
- Don't copy competitor structures wholesale.
- Don't recommend keyword stuffing.
- Don't invent SERP data.
