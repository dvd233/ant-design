#!/usr/bin/env python3
"""Read fixed public source only. Never execute upstream code or install dependencies."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True)
parser.add_argument('--expected', required=True)
parser.add_argument('--out', required=True)
args = parser.parse_args()
source = Path(args.source).resolve()
contract = json.loads(Path(args.expected).read_text())
out = Path(args.out).resolve()
if out == source or source in out.parents:
    raise SystemExit('Refusing to export inside the source checkout')
if out.exists():
    raise SystemExit('Refusing to overwrite an existing output directory')

def git(*argv):
    return subprocess.check_output(['git', '-C', str(source), *argv])

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

assert git('rev-parse', 'HEAD').decode().strip() == contract['base_commit']
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == contract['base_tree']
assert not git('status', '--porcelain', '--untracked-files=all').strip()
rows = []
for row in git('ls-tree', '-r', '-l', '-z', 'HEAD').split(b'\0'):
    if not row:
        continue
    meta, name = row.split(b'\t', 1)
    mode, kind, sha, size = meta.decode().split()
    rows.append({'path': name.decode(), 'mode': mode, 'type': kind, 'git_blob': sha,
                 'bytes': int(size) if size != '-' else None})
blobs = [row for row in rows if row['type'] == 'blob']
assert len(blobs) == contract['source_blob_count']
assert sum(row['bytes'] for row in blobs) == contract['source_blob_bytes']
lock_names = {'package-lock.json', 'npm-shrinkwrap.json', 'yarn.lock', 'pnpm-lock.yaml',
              'bun.lock', 'bun.lockb', 'utoo.lock'}
locks = [row['path'] for row in rows if Path(row['path']).name in lock_names]
assert locks == [], f'Unexpected upstream lockfiles: {locks}'
assert len(contract['export_files']) <= contract['max_export_files']
assert sum(row['bytes'] for row in contract['export_files']) <= contract['max_export_bytes']
tracked = {row['path']: row for row in rows}
verified = []
seen = set()
for item in contract['export_files']:
    name = item['path']
    assert isinstance(name, str) and name and '\\' not in name, name
    relative = PurePosixPath(name)
    assert not relative.is_absolute() and '..' not in relative.parts, name
    assert relative.as_posix() == name and name not in seen, name
    seen.add(name)
    entry = tracked.get(name)
    assert entry is not None and entry['type'] == 'blob', name
    assert entry['mode'] in {'100644', '100755'}, name
    assert entry['git_blob'] == item['git_blob'] and entry['bytes'] == item['bytes'], name
    file = source / name
    assert file.is_file() and not file.is_symlink(), item['path']
    assert source in file.resolve().parents
    data = file.read_bytes()
    assert len(data) == item['bytes'], item['path']
    assert blob(data) == item['git_blob'], item['path']
    verified.append({**item, 'sha256': hashlib.sha256(data).hexdigest()})
out.mkdir()
for item in verified:
    dest = out / 'files' / item['path']
    assert out in dest.resolve().parents, item['path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / item['path'], dest)
summary = {'base_commit': contract['base_commit'], 'base_tree': contract['base_tree'],
           'source_blob_count': len(blobs), 'source_blob_bytes': sum(row['bytes'] for row in blobs),
           'exported_files': len(verified), 'exported_bytes': sum(row['bytes'] for row in verified),
           'export_files': verified, 'tracked_lockfiles': locks,
           'upstream_code_executed': False, 'dependencies_installed': False,
           'browser_docker_or_tests_run': False,
           'pending_install_action_audit': contract['pending_install_action_audit']}
(out / 'inventory.json').write_text(json.dumps(summary, indent=2) + '\n')
(out / 'tracked-files.json').write_text(json.dumps(rows, indent=2) + '\n')
assert sum(file.stat().st_size for file in out.rglob('*') if file.is_file()) <= contract['max_artifact_bytes']
print(json.dumps({key: value for key, value in summary.items() if key != 'export_files'}, indent=2))
