#!/usr/bin/env python3
"""Recreate the two clearly labeled host demonstrations in the deck."""
import csv
import platform
import statistics
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(['make', 'all'], cwd=ROOT, check=True)
CASES = [
    ('Sequential', ['examples/sequential/main', '1048576', '8']),
    ('Permuted', ['examples/random/main', '1048576', '8']),
    ('ijk', ['examples/matmul/main', '256', 'ijk']),
    ('ikj', ['examples/matmul/main', '256', 'ikj']),
]
measurements=[]
for label, args in CASES:
    output = subprocess.check_output(args, cwd=ROOT, text=True).split()[0]
    elapsed=[]
    for _ in range(7):
        t0 = time.perf_counter()
        got = subprocess.check_output(args, cwd=ROOT, text=True).split()[0]
        assert got == output
        elapsed.append((time.perf_counter()-t0)*1000)
    measurements.append({'case':label, 'median_ms':f'{statistics.median(elapsed):.4f}',
                         'checksum':output, 'runs':7})
assert measurements[0]['checksum'] == measurements[1]['checksum']
assert measurements[2]['checksum'] == measurements[3]['checksum']
path=ROOT/'assets/plots/host-measurements.csv'
with path.open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=measurements[0].keys());writer.writeheader();writer.writerows(measurements)
(ROOT/'assets/plots/host-environment.txt').write_text(
    f'Host demonstration, not gem5. {platform.platform()}\n'
    f'Architecture: {platform.machine()}\n'
    'Seven runs per case; median process wall time, includes launch.\n'
    'Compiler flags: see Makefile. These values depend on this host.\n')
print(path)
