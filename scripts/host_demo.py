#!/usr/bin/env python3
"""Time the native examples on this machine and plot them (not gem5)."""
import csv
from pathlib import Path
import platform
import statistics
import subprocess
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PLOTS = ROOT / 'assets/plots'
RUNS = 7
CASES = [
    ('Sequential', ['examples/sequential/main', '1048576', '8']),
    ('Permuted', ['examples/random/main', '1048576', '8']),
    ('ijk', ['examples/matmul/main', '256', 'ijk']),
    ('ikj', ['examples/matmul/main', '256', 'ikj']),
]

subprocess.run(['make', 'all'], cwd=ROOT, check=True)
rows = []
for label, cmd in CASES:
    times = []
    for _ in range(RUNS):
        t0 = time.perf_counter()
        out = subprocess.check_output(cmd, cwd=ROOT, text=True).split()[0]
        times.append((time.perf_counter() - t0) * 1000)
    rows.append({'case': label, 'median_ms': f'{statistics.median(times):.4f}',
                 'checksum': out, 'runs': RUNS})

with (PLOTS / 'host-measurements.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
(PLOTS / 'host-environment.txt').write_text(
    f'Host demonstration, not gem5. {platform.platform()}\n'
    f'Architecture: {platform.machine()}\n'
    f'{RUNS} runs per case; median process wall time, includes launch.\n'
    'Compiler flags: see Makefile. These values depend on this host.\n')

for filename, subset, title in (
    ('host-access-patterns.svg', rows[:2], 'Same data, different order'),
    ('host-matmul.svg', rows[2:], 'Same answer, different loop order'),
):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar([r['case'] for r in subset], [float(r['median_ms']) for r in subset],
           color='#008eae', width=.52)
    ax.set(title=title, ylabel='Host wall time (ms)')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=16)
    ax.yaxis.label.set_size(17)
    ax.title.set_size(21)
    fig.text(.5, .015, f'Example host timing · median of {RUNS} runs · not gem5',
             ha='center', fontsize=12, color='#526b79')
    fig.tight_layout(rect=[0, .06, 1, 1])
    fig.savefig(PLOTS / filename, bbox_inches='tight')
    plt.close(fig)
    print('assets/plots/' + filename)
