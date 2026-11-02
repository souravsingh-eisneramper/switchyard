# Switchyard: Notes

## Purpose
Learning project. Building an LLM cost autopilot that routes requests to the cheapest capable model and measures savings against a fixed baseline. I'm building the router myself (FastAPI, direct provider calls, own ledger) instead of using LiteLLM, to learn how the pieces work.

## Project decisions
- **Baseline model:** Claude Sonnet 5.5
- **Tiers:** tier1 = Haiku 5.5, tier2 = Sonnet 5.5, tier3 = Opus 5.5
- **Models and prices are data**, kept in `policies/models.yaml`, not in code
- **Task tags:** extract, summarize, classify, draft, code, reason
- **Logging policy:** Open (full, truncated, or metadata only; decide before logging client data)
- **Savings per request:** baseline cost minus actual cost, including escalations
- **Control group:** 5% of traffic goes straight to the baseline

## ModelConfig decisions

| Decision | Choice | Reason |
|---|---|---|
| Price units | Per million tokens | Matches how pricing pages list prices, fewer typos |
| Number type | Float | Open: reason not yet written. Test summing 0.1 a million times and decide if the error matters for savings numbers; consider Decimal |
| Cost fields | Input and output only | Cache fields deferred (see limitation below) |
| Tier | String | Open: allowed values, and whether tier belongs on the model or in the routing policy |
| Model ID | String | |
| Provider | String | |
| Latency | Measured in the ledger | It's a measurement, not config, so it won't go stale |
| Extra fields now | Effective date, baseline flag, context window, status | Supports keeping pricing and model options open |

### Known limitation
Cost is calculated from input and output tokens only. Calls that use prompt caching will have their cost misstated until cache prices are added. The ledger will still log `cached_tokens` so the data is there when I add them.

### Open decisions
- Lookup key: model ID alone, or provider plus model ID (and channel, since the same model can have different prices via different channels)
- Allowed tier values, and validation of them
- Allowed status values (e.g. active, testing, deprecated)
- Effective date type, and how to handle price changes over time
- Mutable or frozen dataclass
- Validation rules (empty IDs, negative prices) and where they live
- Failed lookup behavior: return None or raise
- How to add cache fields later: required vs defaulted, and whether a default of 0 could make cached calls look free
- Whether the loader rejects unknown YAML keys
- Naming: use snake_case for all fields and YAML keys

## Ledger fields (planned)
request_id, timestamp, app, task_tag, model_served, tier, provider_channel, prompt_version, input_tokens, output_tokens, cached_tokens, actual_cost, baseline_cost, latency_ms, escalated, escalation_from, outcome, control_group

## Build order
1. ModelConfig dataclass and tests
2. models.yaml and loader
3. Registry lookups
4. Provider client (one call returns text plus usage)
5. Cost function with unit tests, checked against hand calculations and the provider billing page
6. Ledger table and write function
7. FastAPI endpoint with a hard-coded tier
8. Routing rules, escalation, control group, baseline cost

## What I learned
- **`__init__.py`** marks a package and runs once on first import. It isn't a program entrypoint. Scripts use `if __name__ == "__main__"`, packages use `__main__.py`, and installed commands use console scripts.
- **`wheel`** isn't needed in `[build-system] requires` with modern setuptools. Tested by removing it and reinstalling. It also doesn't belong in runtime dependencies.
- **`build-system.requires`** lists tools needed to build the package, while **`project.dependencies`** lists libraries needed to run it.
- **TOML** doesn't allow a table header to appear twice.
- **Extras:** only add dependencies when code uses them. Removed the unused `cli` extra.
- **Package layout:** `src/` layout, installed with `pip install -e ".[test]"`. Verified by importing from outside the repo.

## Git and GitHub troubleshooting
- A 403 on push with working `git ls-remote` means reads work but write authentication fails. Reads can succeed without any login on a public repo.
- `gh auth status` showed the login came from the `GITHUB_TOKEN` environment variable (prefix `ghu_`), which overrides stored logins.
- Fix: unset the variable, `gh auth login`, `gh auth setup-git`, then `git pull --rebase --allow-unrelated-histories` and push.
- **Open:** find out where `GITHUB_TOKEN` is set, since it may return in new terminals.
- Never paste tokens anywhere. Never force-push to get past a rejected push.

## To verify
- Model IDs and prices at docs.claude.com (record the date checked)
- What changed in setuptools 77.0.0 and whether it affects the `license` field
- Firm policy on author email in package metadata and on where this code is hosted
