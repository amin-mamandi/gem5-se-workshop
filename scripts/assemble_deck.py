#!/usr/bin/env python3
"""Combine Bootcamp-style Marp topic files into one presentation."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
parts = sorted((root / 'slides').glob('[0-9][0-9]-*/*.md'))
assert parts, 'No slide modules found'
out = root / '.build'
out.mkdir(exist_ok=True)
header = '---\nmarp: true\ntheme: workshop\npaginate: true\ntitle: Follow the data\n---\n'
combined = []
for file in parts:
    body = re.sub(r'\A---\n.*?\n---\n', '', file.read_text(),
                  count=1, flags=re.S).strip()
    # The assembled source lives in .build: resolve assets against root.
    body = body.replace('../../assets/', '../assets/')
    combined.append(body)
(out / 'complete.md').write_text(header + '\n' + '\n\n---\n\n'.join(combined) + '\n')
print(f'Assembled {len(parts)} modules into .build/complete.md')
