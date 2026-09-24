CC ?= gcc
CFLAGS ?= -O2 -std=c11 -Wall -Wextra -fno-tree-vectorize
GEM5_CC ?= riscv64-linux-gnu-gcc
GEM5_CFLAGS ?= -O2 -std=c11 -Wall -Wextra -fno-tree-vectorize -static -no-pie
PROGRAMS := simple sequential random matmul dram-patterns
.PHONY: all gem5 clean check
all: $(addprefix examples/,$(addsuffix /main,$(PROGRAMS))) examples/simple/cpu_walkthrough
examples/simple/cpu_walkthrough: examples/simple/cpu_walkthrough.c
	$(CC) $(CFLAGS) $< -o $@
gem5: $(addprefix examples/,$(addsuffix /main-gem5,$(PROGRAMS))) examples/simple/cpu_walkthrough-gem5
examples/%-gem5: examples/%.c
	$(GEM5_CC) $(GEM5_CFLAGS) $< -o $@
examples/%/main: examples/%/main.c
	$(CC) $(CFLAGS) $< -o $@
check: all
	@test "$(shell examples/simple/cpu_walkthrough)" = "sum = 30"
	@test "$(shell examples/sequential/main 1024 3)" = "$(shell examples/random/main 1024 3)"
	@test "$(shell examples/matmul/main 16 ijk | cut -d' ' -f1)" = "$(shell examples/matmul/main 16 ikj | cut -d' ' -f1)"
clean:
	rm -f $(addprefix examples/,$(addsuffix /main,$(PROGRAMS))) $(addprefix examples/,$(addsuffix /main-gem5,$(PROGRAMS))) examples/simple/cpu_walkthrough examples/simple/cpu_walkthrough-gem5
