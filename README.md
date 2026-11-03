# Switchyard

[![switchyard-python-ci](https://github.com/souravsingh-eisneramper/switchyard/actions/workflows/main.yml/badge.svg)](https://github.com/souravsingh-eisneramper/switchyard/actions/workflows/main.yml)[![Security Scan](https://github.com/souravsingh-eisneramper/switchyard/actions/workflows/codeql.yml/badge.svg)](https://github.com/souravsingh-eisneramper/switchyard/actions/workflows/codeql.yml)

Switchyard is a Python-based model routing foundation for LLM applications. It is designed to route requests to the most cost-effective model that can handle a given task while keeping pricing, routing decisions, and model metadata explicit and maintainable.

At its current stage, the project focuses on the model registry and validation layer—the core building blocks needed before a full router, evaluator, or gateway is added.

## Why this project exists

Most LLM systems default every request to a single premium model. That is simple, but it is rarely the cheapest or most efficient approach. Switchyard is built around the idea that model selection should be data-driven, measured, and transparent.

The long-term goal is to support:

- task-aware routing by tier
- cost-aware model selection
- provider-neutral configuration
- observability around price/performance tradeoffs
- future quality checks, escalation logic, and routing policies

## Current implementation

This repository already includes the core model configuration layer:

- `Tier` and `Status` enums
- `ModelConfig` dataclass with validation
- Decimal-based price validation for input and output costs
- tests covering valid and invalid configuration inputs

This is the foundation on which a complete router can be built.

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

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

To install the test dependencies as well:

```bash
pip install -e ".[test]"
```

## Quick example

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

This object represents the sort of metadata a routing layer will later use when deciding which model should handle a request.

## Validation and testing

The repository includes unit tests covering the configuration contract.

Run the test suite with:

```bash
pytest
```

The tests validate:

- required string fields and blank values
- enum membership for `Tier` and `Status`
- non-negative and finite price inputs
- positive context windows
- type correctness for model metadata

## Design principles

Switchyard is intentionally strict about data quality. Invalid model definitions fail early rather than causing downstream routing bugs.

The system is designed around a few principles:

- explicit model metadata
- validation at construction time
- cost transparency
- provider-agnostic routing abstractions
- future extensibility for budgets, quality gates, and observability

## Roadmap

The planned path for the project is:

1. YAML-backed model registry and loader
2. cost calculation utilities
3. routing logic by tier and task type
4. provider integration and request execution
5. ledger and telemetry for request cost and latency
6. evaluation, escalation, and quality-control workflows

## Status

This repository is currently in an early, foundational phase. The model registry is implemented and tested, but the full routing system, API surface, and production-grade observability stack are still ahead.

## Notes

A companion `NOTES.md` file captures the project’s design thinking, open decisions, and implementation learnings from the build process.
