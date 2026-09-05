#!/usr/bin/env python3
"""Inventory and package documentation; never packages a playable game or assets."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','.agents','artifacts','Library','Temp','node_modules','__pycache__'}

def main() -> None:
 parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=ROOT/'artifacts'); args=parser.parse_args()
 args.output.mkdir(parents=True,exist_ok=True)
 files=sorted(p for p in ROOT.rglob('*.md') if not EXCLUDED.intersection(p.relative_to(ROOT).parts))
 documents=[]
 for p in files:
  data=p.read_bytes(); text=data.decode('utf-8'); meta={}
  if text.startswith('---\n'):
   for line in text.split('---',2)[1].splitlines():
    match=re.match(r'^([a-z_]+):\s*(.*)$',line)
    if match: meta[match[1]]=match[2].strip('"')
  documents.append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(data),'lines':len(text.splitlines()),'sha256':hashlib.sha256(data).hexdigest(),'metadata':meta,'headings':[{'line':n,'text':line} for n,line in enumerate(text.splitlines(),1) if re.match(r'^#{1,4} ',line)],'open_items':[{'line':n,'text':line} for n,line in enumerate(text.splitlines(),1) if re.search(r'\bOPEN\b|待确认|待裁决|仍未锁|尚未决定',line)]})
 try: commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
 except (subprocess.CalledProcessError,FileNotFoundError): commit='local copy; inspect source report for commit'
 report={'commit':commit,'documents':documents,'count':len(documents),'scope':'Documentation inventory only; game implementation and validation are separate.'}
 (args.output/'document-inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 with zipfile.ZipFile(args.output/'documentation-source.zip','w',zipfile.ZIP_DEFLATED) as archive:
  for p in files: archive.write(p,p.relative_to(ROOT).as_posix())
 # Explicit allowlist: this must not become a game/paid-asset export later.
 package=list(files)
 package.extend(p for directory in ['tools','.github/workflows'] for p in (ROOT/directory).rglob('*') if p.is_file() and p.suffix in {'.py','.yml','.yaml','.json'} and not EXCLUDED.intersection(p.relative_to(ROOT).parts))
 package.extend(p for p in (ROOT/'docs/governance').glob('*.json'))
 with zipfile.ZipFile(args.output/'repository-documentation.zip','w',zipfile.ZIP_DEFLATED) as archive:
  for p in sorted(set(package)): archive.write(p,p.relative_to(ROOT).as_posix())
  for name in ['document-validation.json','document-inventory.json']:
   p=args.output/name
   if p.exists(): archive.write(p,'validation/'+name)
 print(f'Inventoried {len(documents)} Markdown documents at {commit}. No game tests claimed.')
 for item in documents: print(f"{item['path']} | {item['lines']} lines | {item['metadata'].get('doc_id','source/skill')}")

if __name__=='__main__': main()
