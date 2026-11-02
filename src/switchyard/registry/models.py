from dataclasses import dataclass
from decimal import Decimal
from datetime import date
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

@dataclass(frozen=True)
class ModelConfig:
    """Configuration and pricing details for a model.

    Attributes:
        model_id: Identifier for the model.
        provider: Model provider.
        tier: Model tier or classification.
        input_cost_per_million: Input-token cost per million tokens.
        output_cost_per_million: Output-token cost per million tokens.
        effective_date: Date these configuration details take effect.
        baseline_flag: Whether the model is designated as a baseline.
        status: Current status of the model.
        context_window: Maximum context window, in tokens.
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
        """Validate pricing, model ID, and context window.

        Raises:
            ValueError: If either cost or the context window is not positive,
                or if the model ID is ``None``.
        """

        _require_non_blank_str(self.model_id, "model_id")
        _require_non_blank_str(self.provider, "provider")
        
        if not isinstance(self.tier, Tier):
            raise TypeError("tier must be a Tier type Enum")

        if not isinstance(self.status, Status):
            raise TypeError("Status must be a Status type Enum")

        if self.input_cost_per_million < 0:
            raise ValueError("Input Cost of tokens cannot be negative")
        
        if self.output_cost_per_million < 0:
            raise ValueError("Output Cost of tokens cannot be negative")
        
        if self.context_window <= 0:
            raise ValueError("Context Window needs to be a positive number.")
        

