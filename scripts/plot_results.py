#!/usr/bin/env python3
"""Only plot measured summary.csv from run_suite.py; never synthesize data."""
import csv
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['cache-latency', 'cache-size', 'sequential-vs-random',
         'matmul', 'dram-patterns']
LABELS = {
    'cache-latency': ('L1 data latency (cycles)', 'l1d_latency'),
    'cache-size': ('L1 data size', 'l1d_size'),
    'sequential-vs-random': ('Access order', 'program'),
    'matmul': ('Loop order', 'order'),
    'dram-patterns': ('Element stride', 'step'),
}

def plot(experiment):
    csv_path = ROOT / 'experiments' / experiment / 'results/summary.csv'
    if not csv_path.exists():
        raise SystemExit(f'No real measurements at {csv_path}. Run gem5 first.')
    with csv_path.open() as f: rows = list(csv.DictReader(f))
    if not rows: raise SystemExit('Empty measurement file')
    x_title, key = LABELS[experiment]
    labels = [row[key] for row in rows]
    seconds = [float(row['sim_seconds']) for row in rows]
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.bar(labels, seconds, color='#008eae', width=.55)
    ax.set(xlabel=x_title, ylabel='Simulated seconds', title=experiment.replace('-', ' ').title())
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=15)
    ax.xaxis.label.set_size(17); ax.yaxis.label.set_size(17)
    ax.title.set_size(20)
    fig.tight_layout()
    destination = ROOT / 'assets/plots' / (experiment + '.svg')
    fig.savefig(destination, bbox_inches='tight')
    plt.close(fig)
    print(destination)
    if experiment == 'cache-size':
        pairs = [(r, float(r['l1d_misses']) / float(r['l1d_accesses']))
                 for r in rows if r['l1d_misses'] and r['l1d_accesses']
                 and float(r['l1d_accesses']) > 0]
        if len(pairs) == len(rows):
            fig, ax = plt.subplots(figsize=(11, 5.6))
            ax.bar(labels, [p[1] * 100 for p in pairs], color='#008eae', width=.55)
            ax.set(xlabel=x_title, ylabel='L1 data miss rate (%)', title='Cache Size And Miss Rate')
            ax.spines[['top', 'right']].set_visible(False)
            ax.tick_params(labelsize=15)
            fig.tight_layout()
            fig.savefig(ROOT / 'assets/plots/cache-size-miss-rate.svg', bbox_inches='tight')
            plt.close(fig)

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in NAMES:
        raise SystemExit('usage: python3 scripts/plot_results.py ' + '|'.join(NAMES))
    plot(sys.argv[1])
