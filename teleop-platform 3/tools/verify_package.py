"""Check an extracted source package using only Python's standard library."""
import hashlib
from pathlib import Path
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = root / 'MANIFEST.sha256'
    errors = []
    checked = 0
    try:
        lines = manifest.read_text(encoding='utf-8').splitlines()
        for line in lines:
            if not line.strip():
                continue
            digest, name = line.split('  ', 1)
            target = (root / name).resolve()
            if root not in target.parents:
                raise ValueError('invalid manifest path')
            if not target.is_file():
                errors.append('缺少文件：' + name)
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                errors.append('文件已改变：' + name)
            checked += 1
        if not checked:
            errors.append('清单为空')
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    print('已核对 ' + str(checked) + ' 个交付文件。')
    if errors:
        print('\n'.join(errors))
        print('未通过。如果你主动编辑过文件，变化可能是预期的；不要伪造校验结果。')
        return 1
    print('完整性核对通过。此结果不代表硬件或任务验收。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
