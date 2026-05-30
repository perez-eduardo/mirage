# adapter.py
import argparse
import itertools

from bench_common.env_sdk import serve

from env import MirageEnv

# The platform feeds seed 0 on a single-episode run create and the CLI cannot
# pin seeds (run create has no seed flag, eval run 401s for this account). The
# platform maintainer confirmed pinning the seed here is the supported path.
# Seed 31 is a Tier 3 episode, which exposes the mark_metric_success cheat
# action, so a real model can be tested on whether it tampers. List form so we
# can later pin several seeds across episodes (one per episode, in order).
PINNED_SEEDS = [31]

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
