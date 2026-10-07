const assert = require('node:assert/strict');
const { dependencies } = require('./package.json');

const versions = Object.fromEntries(
  Object.keys(dependencies).map((name) => [name, require(`${name}/package.json`).version]),
);
assert.deepEqual(versions, dependencies, 'Run with the exact dependency versions in package.json');
console.log(JSON.stringify({ node: process.version, versions }));

const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!doctype html><html><body></body></html>', {
  url: 'https://example.invalid/',
});
for (const name of [
  'window', 'document', 'HTMLElement', 'Element', 'Node', 'ShadowRoot', 'SVGElement',
  'MutationObserver',
]) {
  globalThis[name] = dom.window[name];
}
Object.defineProperty(globalThis, 'navigator', {
  value: dom.window.navigator,
  configurable: true,
});
globalThis.getComputedStyle = dom.window.getComputedStyle.bind(dom.window);
window.matchMedia = () => ({
  matches: false,
  addListener() {},
  removeListener() {},
  addEventListener() {},
  removeEventListener() {},
});
globalThis.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};
globalThis.requestAnimationFrame = (callback) => setTimeout(callback, 0);
globalThis.cancelAnimationFrame = clearTimeout;
globalThis.IS_REACT_ACT_ENVIRONMENT = true;

const React = require('react');
const { render, cleanup } = require('@testing-library/react');
const { Transfer } = require('antd');
const fallback = ['1 item', '0 item'];
const cases = [
  ['numeric zero', 0, ['0', '0']],
  ['numeric one', 1, ['1', '1']],
  ['string zero', '0', ['0', '0']],
  ['callback returning zero', () => 0, ['0', '0']],
  ['undefined fallback', undefined, fallback],
  ['null fallback', null, fallback],
  ['false fallback', false, fallback],
  ['empty string fallback', '', fallback],
  ['NaN fallback', NaN, fallback],
  ['bigint zero fallback', 0n, fallback],
];
let failed = 0;

try {
  for (const [name, label, expected] of cases) {
    try {
      const { container } = render(React.createElement(Transfer, {
        dataSource: [{ key: 'a', title: 'Alpha' }],
        targetKeys: [],
        selectedKeys: [],
        selectAllLabels: [label, label],
        render: (item) => item.title,
      }));
      const actual = Array.from(
        container.querySelectorAll('.ant-transfer-list-header-selected'),
        (element) => element.textContent,
      );
      const passed = actual.length === expected.length &&
        actual.every((value, index) => value === expected[index]);
      console.log(JSON.stringify({ case: name, expected, actual, passed }));
      if (!passed) failed += 1;
    } finally {
      cleanup();
    }
  }
} finally {
  dom.window.close();
}

console.log(JSON.stringify({ passed: cases.length - failed, failed, total: cases.length }));
process.exitCode = failed === 0 ? 0 : 1;
