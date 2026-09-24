#!/usr/bin/env bash

set -euo pipefail

sudo apt install -y  build-essential scons python3-dev git pre-commit zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    libboost-all-dev  libhdf5-serial-dev python3-pydot python3-venv python3-tk mypy \
    m4 libcapstone-dev libpng-dev libelf-dev pkg-config wget cmake doxygen clang-format \
     gcc-riscv64-linux-gnu libc6-dev-riscv64-cross


cd "$(dirname "$0")"

# Build the examples after installing the RISC-V compiler.
make gem5

if [[ ! -d gem5 ]]; then
    git clone --depth 1 https://github.com/gem5/gem5.git
fi

cd gem5
scons build/RISCV/gem5.fast -j "${JOBS:-4}"
