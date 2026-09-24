"""Upstream RISC-V gem5, single-core Syscall Emulation workshop setup."""
import argparse
from pathlib import Path

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires


class TunableCache(PrivateL1SharedL2CacheHierarchy):
    """Change only L1D hit timing after gem5 creates its classic caches."""

    def __init__(self, size, latency):
        super().__init__(l1d_size=size, l1i_size="32kB", l2_size="256kB")
        # The hierarchy is a SimObject: Python-only fields need a private name.
        self._l1d_latency = latency

    def incorporate_cache(self, board):
        super().incorporate_cache(board)
        for cache in self.l1dcaches:
            cache.tag_latency = self._l1d_latency
            cache.data_latency = self._l1d_latency
            # Keep response_latency at the gem5 class default (1).


parser = argparse.ArgumentParser()
parser.add_argument("--binary", type=Path, required=True)
parser.add_argument("--arg", action="append", default=[])
parser.add_argument("--l1d-size", default="32kB")
parser.add_argument("--l1d-latency", type=int, default=1)
# --cache (default) keeps the L1/L2 caches; --no-cache sends every access to DRAM.
parser.add_argument("--cache", action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()
if args.l1d_latency < 1:
    parser.error("--l1d-latency must be at least 1")
if not args.binary.is_file():
    parser.error(f"binary not found: {args.binary}")

requires(isa_required=ISA.RISCV)
cache = (TunableCache(args.l1d_size, args.l1d_latency) if args.cache else
         NoCache())
board = SimpleBoard(
    clk_freq="2GHz",
    processor=SimpleProcessor(
        cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=1),
    memory=SingleChannelDDR3_1600(size="256MiB"),
    cache_hierarchy=cache,
)
board.set_se_binary_workload(
    BinaryResource(local_path=str(args.binary.resolve()), architecture=ISA.RISCV),
    arguments=args.arg,
)
# Some static Linux toolchains require a newer uname release than gem5's 5.1
# default. This controls the SE syscall response; there is no kernel to boot.
board.get_processor().get_cores()[0].get_simobject().workload[0].release = "5.15.0"
simulator = Simulator(board=board)
simulator.run()
print(f"Exit at tick {simulator.get_current_tick()}: "
      f"{simulator.get_last_exit_event_cause()} "
      f"(code {simulator.get_last_exit_event_code()})")
raise SystemExit(simulator.get_last_exit_event_code())
