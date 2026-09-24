#!/usr/bin/env python3
"""Run a controlled sweep, summarize gem5 stats, then plot real results."""
import argparse
import csv
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'configs/workshop.py'
EXPERIMENTS = {
    'baseline': [('simple', {}, [])],
    'cache-latency': [('sequential', {'l1d-latency': n}, ['16384', '40'])
                      for n in (1, 2, 4, 8)],
    'cache-size': [('sequential', {'l1d-size': s}, ['16384', '40'])
                   for s in ('16kB', '32kB', '64kB', '128kB')],
    'sequential-vs-random': [(p, {}, ['1048576', '4'])
                             for p in ('sequential', 'random')],
    'matmul': [('matmul', {}, ['96', p]) for p in ('ijk', 'ikj')],
    'dram-patterns': [('dram-patterns', {'no-cache': True},
                       ['16384', str(s), '5']) for s in (1, 1025, 8191)],
}


def read_stats(path):
    # The final statistics block is the complete simulator run.
    blocks = path.read_text().split('---------- Begin Simulation Statistics ----------')
    if len(blocks) < 2:
        raise ValueError(f'No statistics block in {path}')
    block = blocks[-1].split('---------- End Simulation Statistics ----------')[0]
    result = {}
    for line in block.splitlines():
        match = re.match(r'^(\S+)\s+([-+\d.eE]+)(?:\s|$)', line)
        if match:
            result[match.group(1)] = float(match.group(2))
    return result


def stat(stats, exact=None, suffix=None):
    if exact in stats:
        return stats[exact]
    if suffix:
        hits = [(key, value) for key, value in stats.items()
                if key.endswith(suffix)]
        if len(hits) == 1:
            return hits[0][1]
        if len(hits) > 1:
            raise ValueError(f'Ambiguous statistic {suffix}: {hits}')
    return ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment', choices=EXPERIMENTS)
    parser.add_argument('--gem5-bin', default=os.environ.get(
        'GEM5_BIN', str(ROOT / 'build/RISCV/gem5.opt')))
    args = parser.parse_args()
    if not args.gem5_bin or not Path(args.gem5_bin).is_file():
        parser.error('Run ./build-gem5.sh or set GEM5_BIN to a RISC-V build')
    # Rebuild the tiny examples so old native/x86 binaries cannot be reused.
    subprocess.run(['make', '-B', 'gem5'], cwd=ROOT, check=True)
    results = ROOT / 'experiments' / args.experiment / 'results'
    results.mkdir(parents=True, exist_ok=True)
    rows = []
    for program, changes, arguments in EXPERIMENTS[args.experiment]:
        label = program + ''.join(f'-{k}-{v}' for k, v in changes.items())
        if args.experiment == 'matmul': label += '-' + arguments[-1]
        if args.experiment == 'dram-patterns': label += '-step-' + arguments[1]
        run_dir = results / label
        run_dir.mkdir(exist_ok=True)
        cmd = [str(Path(args.gem5_bin).resolve()), f'--outdir={run_dir}',
               str(CONFIG), '--binary', str(ROOT / 'examples' / program / 'main-gem5')]
        for key, value in changes.items():
            cmd.append('--' + key)
            if value is not True: cmd.append(str(value))
        for value in arguments: cmd += ['--arg', value]
        print('+', ' '.join(cmd), flush=True)
        with (run_dir / 'command.txt').open('w') as f:
            f.write(' '.join(cmd) + '\n')
        subprocess.run(cmd, check=True, cwd=ROOT)
        stats = read_stats(run_dir / 'stats.txt')
        row = {'label': label, 'program': program,
               'l1d_size': changes.get('l1d-size', '32kB'),
               'l1d_latency': changes.get('l1d-latency', 1),
               'step': arguments[1] if args.experiment == 'dram-patterns' else '',
               'order': arguments[-1] if args.experiment == 'matmul' else '',
               'sim_seconds': stat(stats, exact='simSeconds'),
               'sim_insts': stat(stats, exact='simInsts'),
               'l1d_misses': stat(stats, suffix='l1dcaches.demandMisses::total'),
               'l1d_accesses': stat(stats, suffix='l1dcaches.demandAccesses::total'),
               'dram_reads': stat(stats, suffix='.dram.readBursts'),
               'dram_row_hits': stat(stats, suffix='.dram.readRowHits'),
               'dram_row_hit_rate': stat(stats, suffix='.dram.readRowHitRate')}
        if row['sim_seconds'] == '':
            raise ValueError(f'simSeconds missing from {run_dir}/stats.txt')
        rows.append(row)
    with (results / 'summary.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    print(f'Wrote {results / "summary.csv"}')
    print('Plot: python3 scripts/plot_results.py', args.experiment)


if __name__ == '__main__': main()
