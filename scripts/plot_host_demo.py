#!/usr/bin/env python3
"""Plot recorded host demo CSV without inventing values."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
with (root/'assets/plots/host-measurements.csv').open() as f:
    rows=list(csv.DictReader(f))
for filename,subset,title in (
    ('host-access-patterns.svg', rows[:2], 'Same data, different order'),
    ('host-matmul.svg', rows[2:], 'Same answer, different loop order'),
):
    fig,ax=plt.subplots(figsize=(10,4.8))
    ax.bar([r['case'] for r in subset],[float(r['median_ms']) for r in subset],color='#008eae',width=.52)
    ax.set(title=title,ylabel='Host wall time (ms)')
    ax.spines[['top','right']].set_visible(False)
    ax.tick_params(labelsize=16)
    ax.yaxis.label.set_size(17); ax.title.set_size(21)
    fig.text(.5,.015,'Example host timing · median of 7 runs · not gem5',ha='center',fontsize=12,color='#526b79')
    fig.tight_layout(rect=[0,.06,1,1])
    fig.savefig(root/'assets/plots'/filename,bbox_inches='tight')
    plt.close(fig)
    print(filename)
