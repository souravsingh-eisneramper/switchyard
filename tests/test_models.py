import dataclasses
from datetime import date
from decimal import Decimal

import pytest

from switchyard.registry.models import ModelConfig, Status, Tier

PRICE_FIELDS = ["input_cost_per_million", "output_cost_per_million"]


def make_config(**overrides):
    """Build a valid ModelConfig; override one field per test."""
    fields = dict(
        model_id="claude-haiku-5-5",
        provider="anthropic",
        tier=Tier.TIER1,
        input_cost_per_million=Decimal("1.00"),   # placeholder price
        output_cost_per_million=Decimal("5.00"),  # placeholder price
        effective_date=date(2026, 11, 2),
        baseline_flag=False,
        status=Status.ACTIVE,
        context_window=200_000,
    )
    fields.update(overrides)
    return ModelConfig(**fields)


# --- Valid construction ---

def test_valid_config():
    assert make_config().model_id == "claude-haiku-5-5"


def test_config_accepts_enum_members():
    config = make_config(tier=Tier.TIER3, status=Status.DEPRECATED)
    assert config.tier is Tier.TIER3
    assert config.status is Status.DEPRECATED


def test_config_is_frozen():
    config = make_config()
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.model_id = "something-else"


# --- model_id and provider ---

@pytest.mark.parametrize("field", ["model_id", "provider"])
@pytest.mark.parametrize("bad", [None, 123, True])
def test_wrong_type_raises_type_error(field, bad):
    with pytest.raises(TypeError, match=field):
        make_config(**{field: bad})


@pytest.mark.parametrize("field", ["model_id", "provider"])
@pytest.mark.parametrize("bad", ["", " ", "   ", "\t", "\n"])
def test_blank_raises_value_error(field, bad):
    with pytest.raises(ValueError, match=field):
        make_config(**{field: bad})


# --- tier and status ---

@pytest.mark.parametrize(
    ("field", "bad"),
    [("tier", "TIER1"), ("tier", None), ("status", "ACTIVE"), ("status", None)],
)
def test_tier_and_status_require_enum_members(field, bad):
    with pytest.raises(TypeError, match=field):
        make_config(**{field: bad})


# --- prices ---

@pytest.mark.parametrize("field", PRICE_FIELDS)
@pytest.mark.parametrize("bad", [Decimal("-0.01"), Decimal("-1")])
def test_negative_price_raises_value_error(field, bad):
    with pytest.raises(ValueError, match="negative"):
        make_config(**{field: bad})


@pytest.mark.parametrize("field", PRICE_FIELDS)
def test_zero_price_is_allowed(field):
    # Documents the decision that a zero price is valid.
    assert getattr(make_config(**{field: Decimal("0")}), field) == 0


@pytest.mark.parametrize("field", PRICE_FIELDS)
@pytest.mark.parametrize("bad", ["2.5", 2.5, None])
def test_non_decimal_price_raises_type_error(field, bad):
    with pytest.raises(TypeError, match=field):
        make_config(**{field: bad})


@pytest.mark.parametrize("field", PRICE_FIELDS)
@pytest.mark.parametrize("bad", [Decimal("NaN"), Decimal("Infinity")])
def test_non_finite_price_raises_value_error(field, bad):
    with pytest.raises(ValueError, match=field):
        make_config(**{field: bad})


# --- context window ---

@pytest.mark.parametrize("bad", [0, -1])
def test_non_positive_context_window_raises_value_error(bad):
    with pytest.raises(ValueError, match="positive"):
        make_config(context_window=bad)


@pytest.mark.parametrize("bad", ["100", 1.5, None, True])
def test_non_int_context_window_raises_type_error(bad):
    with pytest.raises(TypeError, match="context_window"):
        make_config(context_window=bad)