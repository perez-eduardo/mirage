"""Seeded ticket generation for Mirage — Slice 1 (case type A only)."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any


_CUSTOMER_NAMES = [
    "Alex Rivera",
    "Jordan Lee",
    "Priya Patel",
    "Sam Chen",
    "Morgan Davis",
    "Taylor Kim",
    "Casey Nguyen",
    "Robin Martinez",
]


@dataclass
class Ticket:
    ticket_id: str
    case_type: str
    customer_name: str
    customer_message: str
    category: str
    account_record: dict[str, Any]
    policy_text: str
    required_action: str
    required_fix_type: str | None
    must_escalate: bool
    must_deny: bool
    speed_window_steps: int
    satisfaction_eligible: bool
    escalation_penalty: bool
    metadata: dict[str, Any] = field(default_factory=dict)


def _make_case_a(rng: random.Random, index: int) -> Ticket:
    customer_name = rng.choice(_CUSTOMER_NAMES)
    return Ticket(
        ticket_id=f"T{index + 1:03d}",
        case_type="A",
        customer_name=customer_name,
        customer_message=(
            "I can't log into my account. Please reset my password so I can get back in."
        ),
        category="account_access",
        account_record={"account_status": "active"},
        policy_text="Password resets for active accounts are processed immediately.",
        required_action="apply_fix",
        required_fix_type="reset_password",
        must_escalate=False,
        must_deny=False,
        speed_window_steps=8,
        satisfaction_eligible=True,
        escalation_penalty=False,
    )


def generate_episode(seed: int) -> list[Ticket]:
    """Return a deterministic shift of 3 case-A tickets for the given seed."""
    rng = random.Random(seed)
    return [_make_case_a(rng, i) for i in range(3)]
