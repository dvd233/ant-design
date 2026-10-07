# Isolated Transfer source inventory

Prepared for review only. Publishing the named branch starts one inventory job through the explicit push trigger. There is no installation, upstream script execution, test, browser, Docker, deployment, commit, or push step in this workflow.

## Bound target

- Fork: dvd233/ant-design
- Repository ID: 1352151349
- Owner ID: 111864431
- Proposed new harness branch: work/transfer-zero-native-inventory-20261007
- Upstream source: ant-design/ant-design at 2d2d49cb6378b6b41c40cd331f63139017ced6e0
- Expected source tree: 8b7bd08e1fa5f60fc10d8590e1ff48c91553a0a2

The branch must be created from an independent tree containing exactly these four files. The workflow rejects extra files or inherited workflows before source checkout. Repository, owner and ref mismatch fail closed. The parent must verify that the proposed branch is new before publication. Existing branches and PR #59173 are outside scope.

## Cost and limits

A shallow checkout reads approximately 58.7 MB of public source blobs (5,041 files) into the isolated hosted runner. Git transport overhead and runner disk usage are separate from this measured source size.

The export whitelist contains exactly 58 text files / 309,653 bytes, each bound to its original Git blob. It includes package/config/setup/helpers/scripts, Transfer source, relevant tests, and three small direct-test snapshots. It excludes demo snapshots and images. Full tracked-file metadata is also exported, with the complete artifact limited to 2 MiB. The whitelist ceiling is 80 files / 512 KiB. The upload explicitly includes hidden files, so approved dotfiles such as `.npmrc`, `.jest.js`, and `.github/workflows/test.yml` are preserved. No full source checkout is uploaded as an artifact. The job timeout is ten minutes and artifact retention is three days.

The complete source tree is verified before export. Missing or modified blobs, new tracked lockfiles, unclean source state, symlinks, duplicate or non-canonical export paths, or size overruns stop the job. Export paths must be relative and match regular-file entries in the fixed tree; every destination must remain inside the output directory. Exported bytes receive SHA-256 checksums.

## Next gate

After the inventory is reviewed, installation needs a separate approval and validation harness. The original setup-utoo action at e7aa4d726a17f79f68aed736476ea5bd68f8ba52 still needs its official action.yml and exact referenced entrypoint reviewed. Do not treat this inventory run as installation approval.

Upstream currently tracks no lockfile and explicitly disables package-lock. Do not invent a lock or mix an old installed antd package into native tests. The eventual baseline, regression-negative and patched-positive checks must use one fresh upstream installation and the same recorded dependency graph.
