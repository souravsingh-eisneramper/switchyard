# Switchyard: Notes

## Purpose
Learning project. Building an LLM cost autopilot that routes requests to the cheapest capable model and measures savings against a fixed baseline. I'm building the router myself (FastAPI, direct provider calls, own ledger) instead of using LiteLLM, to learn how the pieces work.

## Project decisions
- **Baseline model:** Claude Sonnet 5.5
- **Tiers:** tier1 = Haiku 5.5, tier2 = Sonnet 5.5, tier3 = Opus 5.5
- **Models and prices are data**, kept in `policies/models.yaml`, not in code
- **Task tags:** extract, summarize, classify, draft, code, reason
- **Logging policy:** Open (full, truncated, or metadata only; decide before logging client
