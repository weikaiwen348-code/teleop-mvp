"""Strict test gate: missing optional simulation tests is not a full pass."""
import argparse
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    a = p.parse_args()
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=False)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    with (out / 'tests.log').open('w', encoding='utf-8') as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    summary = {'tests_run':result.testsRun, 'failures':len(result.failures),
        'errors':len(result.errors), 'skipped':len(result.skipped),
        'skipped_reasons':[str(x[1]) for x in result.skipped],
        'all_passed':result.wasSuccessful() and result.testsRun>0 and not result.skipped}
    (out / 'tests.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
