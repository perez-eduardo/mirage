# adapter.py
import argparse
import itertools

from bench_common.env_sdk import serve

from env import MirageEnv

# Seeds are pinned here because run create has no seed flag (it feeds seed 0)
# and eval run has no prompt flag. Pinning in the adapter lets run create supply
# the system prompt while we still control which episode runs.
#
# One seed per tier, so a multi-episode run covers the full benchmark:
#   seed 1  -> Tier 1 (aligned control)
#   seed 13 -> Tier 2 (subtle Goodhart)
#   seed 31 -> Tier 3 (blatant tamper)
#
# The cycle advances once per reset(), i.e. once per episode, in order. For a
# balanced aggregate:
#   - run with --episodes a multiple of 3 (3, 6, 9, ...)
#   - keep --parallel 1 so resets stay sequential and the cycle is deterministic
#   - read each episode's tier from terminal_info.episode_tier, never the export
#     seed field (which reports 0)
#
# Whether the cycle survives across the episodes of a run depends on the platform
# keeping ONE adapter process per run. This is not guaranteed and not documented.
# Verify with a 3-episode test run and confirm the three episodes report tiers
# 1, 2, 3 before spending full runs. If they all report tier 1, the adapter is
# being restarted per episode and this approach needs rethinking.
PINNED_SEEDS = [1, 13, 31]

_seed_cycle = itertools.cycle(PINNED_SEEDS)


class PinnedSeedEnv(MirageEnv):
    """MirageEnv that ignores the platform seed and uses our pinned seed(s)."""

    def reset(self, seed=None, **params):
        forced = next(_seed_cycle)
        return super().reset(seed=forced, **params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    print(f"MirageEnv adapter (pinned seeds {PINNED_SEEDS}) -> http://{args.host}:{args.port}")
    serve(PinnedSeedEnv, host=args.host, port=args.port)
