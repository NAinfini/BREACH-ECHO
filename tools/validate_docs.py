#!/usr/bin/env python3
"""Validate BREACH ECHO documentation. Standard library only; no game claims.

Usage: python3 tools/validate_docs.py [--reindex] [--self-test]
Historical source files are immutable and exempt from authoring metadata/links.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = 'docs/治理/完整文档登记.md'
EXCLUDED = {'.git', '.agents', 'artifacts', 'node_modules', 'Library', 'Temp', '__pycache__'}
REQUIRED = {'doc_id', 'doc_type', 'stage', 'updated', 'owner_role', 'canon_basis', 'depends_on'}
STAGES = {'BASELINE', 'REVIEW', 'FUTURE', 'ARCHIVE', 'TEMPLATE'}
PROTECTED = {
 'docs/sources/原始来源-全项目统计与唯一真相-v2.0.md': '99721139befb62405c5b83067463161c9a9817435730d7ad72dddd2015accf0c',
 'docs/sources/原始来源-ChatGPT残酷审查-v1.0.md': '1fd4d10f8f22b2ce0263e26edcba0eb85e554eabd43aec907fa603ff68b87c16',
}

def paths(root: Path) -> list[Path]:
 return sorted(p for p in root.rglob('*.md') if not EXCLUDED.intersection(p.relative_to(root).parts))

def canonical_source_bytes(path: Path) -> bytes:
 """Hash protected text independently of Git/OS newline checkout policy."""
 text=path.read_text(encoding='utf-8')
 return text.replace('\r\n','\n').replace('\r','\n').encode('utf-8')

def metadata(text: str) -> dict[str, str]:
 if not text.startswith('---\n'): return {}
 parts=text.split('---',2)
 if len(parts)<3: return {}
 result={}; lines=parts[1].splitlines(); index=0
 while index<len(lines):
  match=re.match(r'^([a-z_]+):\s*(.*)$',lines[index])
  if not match:
   index+=1; continue
  key,value=match[1],match[2].strip()
  if value:
   result[key]=value; index+=1; continue
  items=[]; cursor=index+1
  while cursor<len(lines):
   item=re.match(r'^\s+-\s*(.*?)\s*$',lines[cursor])
   if not item: break
   raw=item[1]
   try: parsed=json.loads(raw)
   except json.JSONDecodeError: parsed=raw
   items.append(parsed); cursor+=1
  result[key]=json.dumps(items,ensure_ascii=False) if items else ''
  index=cursor
 return result

def prose(text: str) -> str:
 return re.sub(r'(?ms)^(```|~~~).*?^\1\s*$', '', text)

def english_only_prose_lines(text: str) -> list[int]:
 """Find prose-heavy lines that contain no Chinese; keep identifiers and code legal."""
 result=[]; in_frontmatter=False; in_fence=False
 for number,line in enumerate(text.splitlines(),1):
  if number==1 and line.strip()=='---':
   in_frontmatter=True; continue
  if in_frontmatter:
   if line.strip()=='---': in_frontmatter=False
   continue
  if re.match(r'^\s*(```|~~~)',line):
   in_fence=not in_fence; continue
  if in_fence or not line.strip(): continue
  latin_words=re.findall(r'\b[A-Za-z][A-Za-z0-9_-]{2,}\b',line)
  if len(latin_words)>=5 and not re.search(r'[\u4e00-\u9fff]',line): result.append(number)
 return result

def destinations(text: str) -> list[str]:
 return re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)',prose(text))

def local_target(root: Path, path: Path, link: str) -> Path | None:
 parsed=urlsplit(link.strip('<>'))
 if parsed.scheme or parsed.netloc or not parsed.path: return None
 target=(root/parsed.path.lstrip('/')) if parsed.path.startswith('/') else (path.parent/unquote(parsed.path))
 return target.resolve()

def reindex(root: Path) -> None:
 registry=root/REGISTRY
 registry.parent.mkdir(parents=True,exist_ok=True)
 if not registry.exists():
  registry.write_text('---\ndoc_id: GOV-DOCUMENT-REGISTER\ndoc_type: governance\nstage: BASELINE\nupdated: 2026-09-05\nowner_role: 文档治理负责人\ncanon_basis: "当前文档治理基线"\ndepends_on: []\n---\n',encoding='utf-8')
 header=registry.read_text(encoding='utf-8').split('---',2)
 if len(header)<3: raise ValueError('Registry needs valid frontmatter')
 front='---'+header[1]+'---\n\n'
 rows=[]
 for p in paths(root):
  text=p.read_text(encoding='utf-8'); meta=metadata(text)
  rel=p.relative_to(root).as_posix()
  title=next((line[2:].strip() for line in text.splitlines() if line.startswith('# ')),p.stem)
  title=title.replace('|','/').replace('[','(').replace(']',')')
  link=Path(os.path.relpath(p,registry.parent)).as_posix()
  identity=meta.get('doc_id',rel).strip('"')
  stage=meta.get('stage','ARCHIVE' if rel in PROTECTED else 'ENTRY/SKILL').strip('"')
  rows.append(f'| `{identity}` | {stage} | [{title}]({link}) |')
 body='# 完整文档登记\n\n这份登记包含全部 Markdown：根入口、项目技能、现行规格、创作审阅、未来设计、历史来源和模板。`BASELINE` 表示文档权威，不代表游戏已经实现。按角色先读[文档总览](../文档总览.md)，再阅读相关责任文件。两份受保护的原始来源快照保持原文，只用于证据追溯，不是现行设计。\n\n'
 body+=f'自动登记文件数：{len(rows)}。新增或改名后运行 `python3 tools/validate_docs.py --reindex` 更新本表。\n\n'
 body+='| ID / 路径 | 用途 / 状态 | 文档 |\n|---|---|---|\n'+'\n'.join(rows)+'\n'
 registry.write_text(front+body,encoding='utf-8')

def validate(root: Path, protected: dict[str,str] | None=None) -> dict:
 root=root.resolve(); protected=PROTECTED if protected is None else protected
 errors=[]; warnings=[]; ids={}; rule_ids={}; dependency_graph={}; files=paths(root); links_checked=0; dependencies_checked=0
 for rel,digest in protected.items():
  p=root/rel
  if not p.is_file() or hashlib.sha256(canonical_source_bytes(p)).hexdigest()!=digest:
   errors.append(f'PROTECTED_SOURCE: {rel} missing or changed')
 for p in files:
  rel=p.relative_to(root).as_posix()
  try: text=p.read_text(encoding='utf-8')
  except UnicodeError:
   errors.append(f'UTF8: {rel}'); continue
  if rel in protected: continue
  for line_number in english_only_prose_lines(text):
   errors.append(f'LANGUAGE: {rel}:{line_number}: English-only prose in maintained document')
  meta=metadata(text)
  if rel.startswith('docs/'):
   dependency_graph[rel]=[]
   missing=sorted(REQUIRED-set(meta))
   if missing: errors.append(f'METADATA: {rel}: missing {missing}')
   if meta.get('stage') not in STAGES: errors.append(f'STAGE: {rel}: {meta.get("stage")}')
   if rel.startswith('docs/未来扩展/') and meta.get('stage')!='FUTURE':
    errors.append(f'FUTURE_SCOPE: {rel}: future planning must remain FUTURE')
   if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',meta.get('updated','')): errors.append(f'DATE: {rel}')
   ident=meta.get('doc_id')
   if ident in ids: errors.append(f'DUPLICATE_ID: {ident}: {ids[ident]} and {rel}')
   if ident: ids[ident]=rel
   if ident and re.fullmatch(r'(?:DDD|ADR|DEC)-?\d+',ident,re.IGNORECASE):
    errors.append(f'NON_SEMANTIC_DOC_ID: {rel}: {ident}')
   if meta.get('doc_type')=='discussion':
    errors.append(f'DISCUSSION_DOCUMENT: {rel}')
   if re.match(r'(?i)^(?:ddd|adr|dec|doc)[-_]?\d',p.stem) or re.match(r'^\d',p.stem):
    errors.append(f'NON_SEMANTIC_FILENAME: {rel}')
   try:
    deps=json.loads(meta.get('depends_on','[]'))
    if not isinstance(deps,list) or not all(isinstance(x,str) for x in deps): raise ValueError('expected string list')
    for dep in deps:
     dependencies_checked+=1
     target=local_target(root,p,dep)
     if target is None or not target.is_file() or not target.is_relative_to(root):
      errors.append(f'DEPENDENCY: {rel} -> {dep}')
     else: dependency_graph[rel].append(target.relative_to(root).as_posix())
   except (ValueError,TypeError): errors.append(f'DEPENDENCY_FORMAT: {rel}')
  for rule_id in re.findall(r'(?m)^([A-Z][A-Z0-9]*-[0-9]{3})\s*·',text):
   if rule_id in rule_ids: errors.append(f'DUPLICATE_RULE_ID: {rule_id}: {rule_ids[rule_id]} and {rel}')
   else: rule_ids[rule_id]=rel
  if meta.get('stage')!='ARCHIVE':
   if re.search(r'DDD-\d{4}|SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION',text):
    errors.append(f'STALE_FINALIZATION_REFERENCE: {rel}')
  for link in destinations(text):
   try: target=local_target(root,p,link)
   except ValueError:
    errors.append(f'LINK_SYNTAX: {rel} -> {link}'); continue
   if target is None: continue
   links_checked+=1
   if not target.is_relative_to(root) or not target.exists(): errors.append(f'BROKEN_LINK: {rel} -> {link}')
  if meta.get('stage')=='BASELINE' and meta.get('doc_type')!='evidence' and re.search(r'(?:·\s*OPEN\b|\|\s*OPEN\s*\|)',prose(text)):
   warnings.append(f'HISTORICAL_OR_SCOPED_OPEN_REVIEW: {rel}')
 visiting=set(); visited=set(); stack=[]; cycles=set()
 def visit(node: str) -> None:
  if node in visited: return
  if node in visiting:
   start=stack.index(node)
   cycle=stack[start:]+[node]
   key=tuple(sorted(set(cycle)))
   if key not in cycles:
    cycles.add(key); errors.append('DEPENDENCY_CYCLE: '+' -> '.join(cycle))
   return
  visiting.add(node); stack.append(node)
  for target in dependency_graph.get(node,[]):
   if target in dependency_graph: visit(target)
  stack.pop(); visiting.remove(node); visited.add(node)
 for node in sorted(dependency_graph): visit(node)
 registry=root/REGISTRY
 if not registry.is_file(): errors.append('REGISTRY: missing document register')
 else:
  text=registry.read_text(encoding='utf-8')
  registered=[]
  for line in text.splitlines():
   if not line.startswith('| `'): continue
   for link in destinations(line):
    target=local_target(root,registry,link)
    if target is not None: registered.append(target)
  expected=set(p.resolve() for p in files)
  missing=expected-set(registered); extra=set(registered)-expected
  for p in sorted(missing): errors.append('UNREGISTERED: '+p.relative_to(root).as_posix())
  for p in sorted(extra): errors.append('REGISTRY_EXTRA: '+str(p))
  if len(registered)!=len(set(registered)): errors.append('REGISTRY_DUPLICATE: a document has multiple rows')
 decision_index=root/'docs/治理/当前决策登记.md'
 if decision_index.exists():
  links={local_target(root,decision_index,l) for l in destinations(decision_index.read_text(encoding='utf-8'))}
  for p in (root/'docs/治理/选型依据').glob('*.md'):
   if p.resolve() not in links: errors.append('DECISION_NOT_INDEXED: '+p.name)
 checks={
  'docs/玩法/玩家配装与输入.md':['| 官方 Weapon / Utility / Signature | 2 / 2 / 1'],
  'docs/技术/网络权威存档与版本固定.md':['**具体网络provider、选主算法、迁移快照频率和安全校验仍未锁。**'],
 }
 for rel,forbidden in checks.items():
  p=root/rel
  if p.exists():
   text=p.read_text(encoding='utf-8')
   for phrase in forbidden:
    if phrase in text: errors.append(f'SUPERSEDED_CONTRACT: {rel}: {phrase}')
 return {'status':'PASS' if not errors else 'FAIL','markdown_files':len(files),'unique_doc_ids':len(ids),'relative_links_checked':links_checked,'dependencies_checked':dependencies_checked,'protected_sources_checked':len(protected),'errors':errors,'warnings':warnings,'scope':'Document structure and selected contradiction guards only. No game, legal, security or independent-review validation.'}

class ValidatorTests(unittest.TestCase):
 def setUp(self) -> None:
  self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
  p=self.root/'docs/文档总览.md'; p.parent.mkdir()
  p.write_text('---\ndoc_id: DOC-A\ndoc_type: guide\nstage: BASELINE\nupdated: 2026-09-05\nowner_role: Test\ncanon_basis: Test\ndepends_on: []\n---\n\n# A\n',encoding='utf-8')
  reindex(self.root)
 def tearDown(self) -> None: self.temp.cleanup()
 def test_valid_fixture(self) -> None: self.assertFalse(validate(self.root,{})['errors'])
 def test_broken_link_is_rejected(self) -> None:
  p=self.root/'docs/文档总览.md'; p.write_text(p.read_text(encoding='utf-8')+'\n[missing](absent.md)\n',encoding='utf-8')
  self.assertTrue(any(e.startswith('BROKEN_LINK') for e in validate(self.root,{})['errors']))
 def test_duplicate_id_is_rejected(self) -> None:
  p=self.root/'docs/其他.md'; p.write_text((self.root/'docs/文档总览.md').read_text()); reindex(self.root)
  self.assertTrue(any(e.startswith('DUPLICATE_ID') for e in validate(self.root,{})['errors']))
 def test_duplicate_rule_id_is_rejected(self) -> None:
  first=self.root/'docs/文档总览.md'
  first.write_text(first.read_text(encoding='utf-8')+'\nRULE-001 · DECIDED.\n',encoding='utf-8')
  second=self.root/'docs/其他.md'
  second.write_text(first.read_text(encoding='utf-8').replace('DOC-A','DOC-B'),encoding='utf-8')
  reindex(self.root)
  self.assertTrue(any(e.startswith('DUPLICATE_RULE_ID') for e in validate(self.root,{})['errors']))
 def test_bad_dependency_is_rejected(self) -> None:
  p=self.root/'docs/文档总览.md'; p.write_text(p.read_text(encoding='utf-8').replace('depends_on: []','depends_on: ["缺失.md"]'),encoding='utf-8')
  self.assertTrue(any(e.startswith('DEPENDENCY:') for e in validate(self.root,{})['errors']))
 def test_dependency_cycle_is_rejected(self) -> None:
  first=self.root/'docs/文档总览.md'; second=self.root/'docs/其他.md'
  first.write_text(first.read_text(encoding='utf-8').replace('depends_on: []','depends_on: ["其他.md"]'),encoding='utf-8')
  second.write_text(first.read_text(encoding='utf-8').replace('DOC-A','DOC-B').replace('depends_on: ["其他.md"]','depends_on: ["文档总览.md"]'),encoding='utf-8')
  reindex(self.root)
  self.assertTrue(any(e.startswith('DEPENDENCY_CYCLE:') for e in validate(self.root,{})['errors']))
 def test_unregistered_file_is_rejected(self) -> None:
  p=self.root/'docs/其他.md'; p.write_text((self.root/'docs/文档总览.md').read_text().replace('DOC-A','DOC-B'))
  self.assertTrue(any(e.startswith('UNREGISTERED') for e in validate(self.root,{})['errors']))
 def test_source_mutation_is_rejected(self) -> None:
  p=self.root/'source.txt'; p.write_text('original')
  digest=hashlib.sha256(p.read_bytes()).hexdigest(); p.write_text('changed')
  self.assertTrue(any(e.startswith('PROTECTED_SOURCE') for e in validate(self.root,{'source.txt':digest})['errors']))
 def test_protected_source_hash_ignores_checkout_newlines(self) -> None:
  p=self.root/'source.txt'; p.write_bytes(b'first\r\nsecond\r\n')
  digest=hashlib.sha256(b'first\nsecond\n').hexdigest()
  self.assertFalse(any(e.startswith('PROTECTED_SOURCE') for e in validate(self.root,{'source.txt':digest})['errors']))
 def test_code_examples_are_not_links(self) -> None:
  p=self.root/'docs/文档总览.md'; p.write_text(p.read_text(encoding='utf-8')+'\n```text\n[example](missing.md)\n```\n',encoding='utf-8')
  self.assertFalse(validate(self.root,{})['errors'])
 def test_english_only_prose_is_rejected(self) -> None:
  p=self.root/'docs/文档总览.md'
  p.write_text(p.read_text(encoding='utf-8')+'\nThis maintained paragraph must be Chinese.\n',encoding='utf-8')
  self.assertTrue(any(e.startswith('LANGUAGE:') for e in validate(self.root,{})['errors']))
 def test_numeric_decision_id_is_rejected(self) -> None:
  p=self.root/'docs/文档总览.md'
  p.write_text(p.read_text(encoding='utf-8').replace('DOC-A','DDD-0008'),encoding='utf-8')
  reindex(self.root)
  self.assertTrue(any(e.startswith('NON_SEMANTIC_DOC_ID:') for e in validate(self.root,{})['errors']))
 def test_discussion_document_is_rejected(self) -> None:
  p=self.root/'docs/文档总览.md'
  p.write_text(p.read_text(encoding='utf-8').replace('doc_type: guide','doc_type: discussion'),encoding='utf-8')
  reindex(self.root)
  self.assertTrue(any(e.startswith('DISCUSSION_DOCUMENT:') for e in validate(self.root,{})['errors']))
 def test_future_planning_is_preserved_as_future(self) -> None:
  p=self.root/'docs/未来扩展/未来模式.md'; p.parent.mkdir()
  text=(self.root/'docs/文档总览.md').read_text(encoding='utf-8')
  p.write_text(text.replace('DOC-A','FUTURE-MODE').replace('stage: BASELINE','stage: FUTURE'),encoding='utf-8')
  reindex(self.root)
  self.assertFalse(validate(self.root,{})['errors'])
  p.write_text(p.read_text(encoding='utf-8').replace('stage: FUTURE','stage: BASELINE'),encoding='utf-8')
  self.assertTrue(any(e.startswith('FUTURE_SCOPE:') for e in validate(self.root,{})['errors']))

def main() -> int:
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--reindex',action='store_true'); parser.add_argument('--self-test',action='store_true')
 args=parser.parse_args()
 if args.self_test:
  result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ValidatorTests))
  return 0 if result.wasSuccessful() else 1
 if args.reindex: reindex(ROOT)
 report=validate(ROOT)
 out=ROOT/'artifacts'; out.mkdir(exist_ok=True)
 (out/'document-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f"{report['status']}: {report['markdown_files']} Markdown, {report['relative_links_checked']} relative links, {report['dependencies_checked']} dependencies, {report['protected_sources_checked']} protected sources")
 for error in report['errors']: print(error)
 print(f"{len(report['warnings'])} scoped/historical OPEN references require semantic review; not automatically promoted or deleted.")
 print(report['scope'])
 return 0 if not report['errors'] else 1

if __name__=='__main__': sys.exit(main())
