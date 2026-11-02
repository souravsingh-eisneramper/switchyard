# Switchyard

Switchyard is a Python project for building an LLM routing layer that can choose the best model for a task based on cost, quality, and latency. The codebase currently focuses on the model registry and validation layer that a router will eventually use.

The core idea is simple: keep model metadata, pricing, and validation in one place so application code can route by abstract tiers such as `tier1`, `tier2`, and `tier3` instead of hard-coding provider-specific model names.

## Why Switchyard?

Most LLM spending is driven by defaulting every request to a premium model, even when a smaller or cheaper model could handle the task. Switchyard is designed to make that tradeoff explicit and measurable.

The project aims to support:

- cost-aware model routing
- tier-based decision making
- provider-agnostic model configuration
- transparent pricing metadata
- future expansion into routing policies and evaluation logic

## Current state

This repository is still in an early stage. The implemented foundation is the typed model registry:

- `Tier` and `Status` enums
- `ModelConfig` dataclass with validation
- Decimal-based pricing validation for input/output cost
- tests covering expected acceptable and invalid inputs

This is not yet a complete production router or API gateway, but it establishes the data model that the rest of the system can build on.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you want the test dependencies as well:

```bash
pip install -e ".[test]"
```

## Example usage

```python
from datetime import date
from decimal import Decimal

from switchyard.registry.models import ModelConfig, Status, Tier

config = ModelConfig(
    model_id="claude-haiku-5-5",
    provider="anthropic",
    tier=Tier.TIER1,
    input_cost_per_million=Decimal("1.00"),
    output_cost_per_million=Decimal("5.00"),
    effective_date=date(2026, 11, 2),
    baseline_flag=False,
    status=Status.ACTIVE,
    context_window=200_000,
)

print(config.model_id)
print(config.tier)
```

This example demonstrates the core model metadata the router will eventually consume.

## Project structure

```text
.
├── README.md
├── NOTES.md
├── pyproject.toml
├── src/
│   └── switchyard/
│       └── registry/
│           └── models.py
└── tests/
    └── test_models.py
```

## Validation and testing

The repository includes unit tests for the validation rules around model configuration.

Run them with:

```bash
pytest
```

The tests cover:

- required string fields and blank values
- enum validation for `Tier` and `Status`
- negative and non-finite pricing values
- positive context-window checks
- type validation for model metadata

## Roadmap

Planned work includes:

- YAML-backed model registry and loader
- cost calculation utilities
- routing logic by tier and task
- provider integration and request execution
- ledger and observability for request cost and latency
- production-quality evaluation and escalation policies

## Notes

This repository is intentionally opinionated about correctness and data integrity. The config objects are validated at construction time so invalid model definitions fail early instead of slipping into routing logic.

The project is best viewed as a foundation for an LLM cost autopilot and routing system rather than a finished application.
