from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum, auto


class Status(StrEnum):
    ACTIVE = auto()
    TESTING = auto()
    DEPRECATED = auto()


class Tier(StrEnum):
    TIER1 = auto()
    TIER2 = auto()
    TIER3 = auto()


def _require_non_blank_str(value, field_name):
    """Raise TypeError if value is not a str, ValueError if it is blank."""
    if not isinstance(value, str):
        raise TypeError(
            f"{field_name} must be a str, got {type(value).__name__}"
        )
    if not value.strip():
        raise ValueError(f"{field_name} must not be blank, got {value!r}")


def _require_enum_member(value, enum_cls, field_name):
    """Raise TypeError unless value is a member of enum_cls."""
    if not isinstance(value, enum_cls):
        raise TypeError(
            f"{field_name} must be a {enum_cls.__name__}, "
            f"got {type(value).__name__}"
        )


def _require_non_negative_decimal(value, field_name):
    """Raise TypeError if not a Decimal, ValueError if not finite or negative.

    Order matters: the type check comes first so the comparison never sees a
    bad type, and the finite check comes before the comparison because
    comparing NaN raises decimal.InvalidOperation.
    """
    if not isinstance(value, Decimal):
        raise TypeError(
            f"{field_name} must be a Decimal, got {type(value).__name__}"
        )
    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite, got {value!r}")
    if value < 0:
        raise ValueError(f"{field_name} must not be negative, got {value!r}")


def _require_positive_int(value, field_name):
    """Raise TypeError if not an int (bool excluded), ValueError if <= 0."""
    # bool is a subclass of int, so True would pass a plain isinstance check.
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(
            f"{field_name} must be an int, got {type(value).__name__}"
        )
    if value <= 0:
        raise ValueError(
            f"{field_name} must be a positive number, got {value!r}"
        )


@dataclass(frozen=True)
class ModelConfig:
    """Configuration and pricing details for a model.

    Prices are in USD per million tokens (confirm this matches your
    pricing source). The dataclass validates but does not convert: the
    loader must supply real Decimal, Tier, and Status values.

    Attributes:
        model_id: Identifier for the model.
        provider: Model provider (free text).
        tier: Routing tier, a Tier member.
        input_cost_per_million: Input-token price per million tokens.
        output_cost_per_million: Output-token price per million tokens.
        effective_date: Date these configuration details take effect.
        baseline_flag: Whether the model is designated as the baseline.
        status: Lifecycle status, a Status member.
        context_window: Maximum context window, in tokens.

    Raises:
        TypeError: If a field has the wrong type (for example a plain str
            where a Tier, Status, or Decimal is required).
        ValueError: If a string is blank, a price is negative or not
            finite, or the context window is not positive.
    """

    model_id: str
    provider: str
    tier: Tier
    input_cost_per_million: Decimal
    output_cost_per_million: Decimal
    effective_date: date
    baseline_flag: bool
    status: Status
    context_window: int

    def __post_init__(self):
        _require_non_blank_str(self.model_id, "model_id")
        _require_non_blank_str(self.provider, "provider")
        _require_enum_member(self.tier, Tier, "tier")
        _require_enum_member(self.status, Status, "status")
        _require_non_negative_decimal(
            self.input_cost_per_million, "input_cost_per_million"
        )
        _require_non_negative_decimal(
            self.output_cost_per_million, "output_cost_per_million"
        )
        _require_positive_int(self.context_window, "context_window")