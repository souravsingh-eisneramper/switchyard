# Switchyard

**An LLM cost autopilot.** Switchyard sits between your apps and your language models, sends each request to the cheapest model that can handle it, and measures exactly how much that saves.

## Why

Most LLM spend goes to a single default model, even for tasks a smaller model handles equally well. Switchyard routes by task, checks the result, escalates only when needed, and reports savings against a fixed baseline.

## How it works

```
App → Gateway (LiteLLM) → Router → Model tier → Quality check → Response
                             │                        │
                             └──── Cost ledger ◄──────┘
```

| Tier | Typical use | Model |
|---|---|---|
| tier1 | Classification, extraction, reformatting | Claude Haiku 5.5 |
| tier2 (baseline) | Writing, analysis, summarization, most coding | Claude Sonnet 5.5 |
| tier3 | Multi-step reasoning, hard coding, high-stakes work | Claude Opus 5.5 |

Apps request a tier alias (`tier1`, `tier2`, `tier3`), never a specific model. Models, prices, and providers live in config, so they can be swapped without touching app code.

## Principles

- **Measure first.** Log every request before routing any of them.
- **Quality gates savings.** A cheaper model is promoted to a tier only after passing the golden-set eval.
- **Models and prices are data.** Versioned in `policies/models.yaml`, with effective dates.
- **Stay portable.** Multiple providers and channels, with failover.
- **Honest accounting.** Escalations count toward cost, and 5% of traffic goes to the baseline as a control group.

## Decisions

- **Baseline model:** Claude Sonnet 5.5
- **Task tags:** `extract`, `summarize`, `classify`, `draft`, `code`, `reason`
- **Logging policy:** _[full | truncated | metadata only: decide before logging client data]_
- **Savings per request:** baseline cost minus actual cost, including escalations

## Ledger fields

`request_id, timestamp, app, task_tag, model_served, tier, provider_channel, prompt_version, input_tokens, output_tokens, cached_tokens, actual_cost, baseline_cost, latency_ms, escalated, escalation_from, outcome, control_group`

## Quick start

```bash
cp .env.example .env        # add ANTHROPIC_API_KEY and LITELLM_MASTER_KEY
docker compose up -d
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"tier2","messages":[{"role":"user","content":"Hello"}],
       "metadata":{"tags":["summarize","app:test"]}}'
```

## Roadmap

- [ ] Phase 1: Gateway and cost ledger
- [ ] Phase 2: Golden set and eval harness
- [ ] Phase 3: Rules-based router
- [ ] Phase 4: Quality checks, escalation, shadow mode
- [ ] Phase 5: Canary rollout, budgets, alerts
- [ ] Phase 6: Learned routing, caching, batching

## Repo layout

```
gateway/    LiteLLM config and middleware
router/     classifier, policy engine, escalation
policies/   routing.yaml, models.yaml, budgets.yaml
eval/       golden sets, replay scripts, scorers
ledger/     DB schema and cost calculations
dashboards/ Grafana / Metabase exports
tests/
```

## Status

Early development. Phase 1 in progress.
