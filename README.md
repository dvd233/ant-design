# Ant Design Transfer: numeric-zero custom labels

A minimal reproduction of `Transfer` ignoring a direct numeric `0` in `selectAllLabels`.

## Run

Use Node.js 20 or newer. From this directory:

```sh
npm install
npm test
```

All six direct dependencies are pinned to the versions used for the reproduction. This standalone example has no lockfile; transitive dependencies are not frozen. If these exact dependencies are already available, `node repro.cjs` also works through standard Node module resolution, including `NODE_PATH`.

The command renders the real published `antd@6.6.5` Transfer in JSDOM with React/ReactDOM 19.3.0. It starts no server or browser and makes no network requests. Only platform APIs missing from JSDOM are stubbed; Transfer and its label computation are not mocked or patched.

`App.tsx` is the equivalent UI example for an existing React/Ant Design application. It is not a separate executable or a configured browser build.

## Expected and actual behavior

Given one source item, no target items, and `selectAllLabels={[0, 0]}`:

- Expected header labels: `["0", "0"]`
- Actual header labels: `["1 item", "0 item"]`

The script intentionally exits with status **1** on the affected release. Its summary is:

```json
{"passed":9,"failed":1,"total":10}
```

The sole failed case is `numeric zero`. Numeric `1`, string `'0'`, and callbacks returning `0` work correctly. Six compatibility controls document the current fallback for `undefined`, `null`, `false`, an empty string, `NaN`, and bigint `0n`.

A practical use case is passing selected-item counts directly as labels. When a count reaches zero, the displayed custom count unexpectedly changes to the default item-count text.

## Current source and validation scope

The same truthiness guard is present in [Section.tsx at commit 2d2d49cb6378b6b41c40cd331f63139017ced6e0](https://github.com/ant-design/ant-design/blob/2d2d49cb6378b6b41c40cd331f63139017ced6e0/components/transfer/Section.tsx#L319-L325). The [API documentation](https://github.com/ant-design/ant-design/blob/2d2d49cb6378b6b41c40cd331f63139017ced6e0/components/transfer/index.en-US.md#L60) permits ReactNode values for `selectAllLabels`.

This is an executable published-package reproduction. It is not the original repository's test suite, browser/image verification, or CI. No candidate implementation patch is included.

This reproduction and report were prepared with AI assistance. The results above were obtained by running the script with existing offline dependencies.
