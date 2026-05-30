"""Deterministic Slice 1 smoke test — no LLM, no network."""

from __future__ import annotations

from typing import Any

from env import MirageEnv


TERMINAL_FIELDS = [
    "true_success",
    "true_resolution_rate",
    "apparent_score",
    "apparent_true_gap",
    "premature_close",
    "steps",
    "tickets_truly_resolved",
    "failure_label",
]


def _drive(env: MirageEnv, actions_per_ticket: list[dict[str, Any]]):
    """Replay the per-ticket action sequence until the env terminates."""
    result = None
    safety_cap = 200
    steps_taken = 0
    while True:
        for action in actions_per_ticket:
            result = env.step(action)
            steps_taken += 1
            if result.terminated or result.truncated:
                return result
            if steps_taken >= safety_cap:
                raise RuntimeError("Safety cap hit before termination.")


def _summarize(label: str, result) -> None:
    info = result.info
    print(f"=== {label} ===")
    print(f"terminated: {result.terminated}")
    print(f"truncated:  {result.truncated}")
    print(f"final proxy_score: {info.get('proxy_score')}")
    print("Terminal fields:")
    for key in TERMINAL_FIELDS:
        print(f"  {key}: {info.get(key)!r}")
    print(f"Full terminal info: {info}")
    print()


def run_correct_path() -> None:
    env = MirageEnv()
    env.reset(seed=1)
    actions = [
        {"action": "lookup_account"},
        {"action": "apply_fix", "fix_type": "reset_password"},
        {"action": "respond_user", "message": "Done"},
        {"action": "resolve_ticket", "resolution_code": "fixed"},
    ]
    result = _drive(env, actions)
    _summarize("CORRECT PATH (lookup -> fix -> respond -> resolve)", result)
    env.close()


def run_lazy_path() -> None:
    env = MirageEnv()
    env.reset(seed=1)
    actions = [
        {"action": "resolve_ticket", "resolution_code": "fixed"},
    ]
    result = _drive(env, actions)
    _summarize("LAZY PATH (resolve only, no fix)", result)
    env.close()


if __name__ == "__main__":
    run_correct_path()
    run_lazy_path()
