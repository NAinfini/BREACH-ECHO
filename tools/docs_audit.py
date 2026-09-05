#!/usr/bin/env python3
"""Inventory documentation without modifying source files (Python standard library)."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def inventory() -> dict:
    documents = []
    for path in sorted(ROOT.rglob('*.md')):
        if any(part in {'.git', 'artifacts', 'Library', 'Temp', 'node_modules'} for part in path.relative_to(ROOT).parts):
            continue
        data = path.read_bytes()
        text = data.decode('utf-8')
        lines = text.splitlines()
        metadata = {}
        if lines and lines[0] == '---':
            for line in lines[1:]:
                if line == '---':
                    break
                match = re.match(r'^([a-z_]+):\s*(.*)$', line)
                if match:
                    metadata[match[1]] = match[2].strip('"')
        documents.append({
            'path': path.relative_to(ROOT).as_posix(),
            'bytes': len(data), 'lines': len(lines),
            'sha256': hashlib.sha256(data).hexdigest(),
            'metadata': metadata,
            'headings': [{'line': n, 'text': line} for n, line in enumerate(lines, 1) if re.match(r'^#{1,4} ', line)],
            'open_items': [{'line': n, 'text': line} for n, line in enumerate(lines, 1) if re.search(r'\bOPEN\b|待确认|待裁决|仍未锁|尚未决定', line)],
        })
    return {'documents': documents, 'count': len(documents)}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = inventory()
    (args.output / 'document-inventory.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with zipfile.ZipFile(args.output / 'documentation-source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for item in report['documents']:
            archive.write(ROOT / item['path'], item['path'])
    print(f"Inventoried {report['count']} Markdown documents. This is not a semantic approval or game validation.")
    for item in report['documents']:
        print(f"{item['path']} | {item['lines']} lines | {item['metadata'].get('doc_id', 'source/skill')} | {len(item['open_items'])} unresolved-reference lines")

if __name__ == '__main__':
    main()
