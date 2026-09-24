#!/usr/bin/env python3
"""Plot one experiment from results/<experiment>/*/stats.txt (made by sweep-se.sh)."""
from pathlib import Path
import re
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
X_TITLES = {
    'cache-latency': 'L1 data latency (cycles)',
    'cache-size': 'L1 data size',
    'sequential-vs-random': 'Access order',
    'matmul': 'Loop order',
    'dram-patterns': 'Stride (words)',
}


def read_stats(path):
    stats = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            try: stats[parts[0]] = float(parts[1])
            except ValueError: pass
    return stats


def find(stats, suffix):
    return next((v for k, v in stats.items() if k.endswith(suffix)), None)


def order(name):
    match = re.match(r'\d+', name)
    return (0, int(match.group()), name) if match else (1, 0, name)


def bar(labels, values, x_title, y_title, title, filename):
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.bar(labels, values, color='#008eae', width=.55)
    ax.set(xlabel=x_title, ylabel=y_title, title=title)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    fig.savefig(ROOT / 'assets/plots' / filename, bbox_inches='tight')
    plt.close(fig)
    print('assets/plots/' + filename)


if len(sys.argv) != 2 or sys.argv[1] not in X_TITLES:
    sys.exit('usage: python3 scripts/plot_results.py ' + '|'.join(X_TITLES))
experiment = sys.argv[1]
runs = sorted((ROOT / 'results' / experiment).glob('*/stats.txt'),
              key=lambda p: order(p.parent.name))
if not runs:
    sys.exit(f'No results in results/{experiment}/. Run ./sweep-se.sh first.')

labels = [p.parent.name for p in runs]
stats = [read_stats(p) for p in runs]
title = experiment.replace('-', ' ').title()
bar(labels, [s['simSeconds'] for s in stats], X_TITLES[experiment],
    'Simulated seconds', title, experiment + '.svg')
if experiment == 'cache-size':
    rates = [find(s, 'l1dcaches.demandMissRate::total') for s in stats]
    bar(labels, [r * 100 for r in rates], X_TITLES[experiment],
        'L1 data miss rate (%)', 'Cache Size And Miss Rate',
        'cache-size-miss-rate.svg')
