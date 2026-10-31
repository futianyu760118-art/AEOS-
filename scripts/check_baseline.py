#!/usr/bin/env python3
"""AEOS controlled baseline integrity checker. Requires Python 3 stdlib only."""
from pathlib import Path
import argparse, hashlib, sys
ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
 "AEOS_V7.2_分模块分阶段具体执行方案_V1.0.docx": (528704, "77fce188fa7f5f8780c5324dc73a5a89afdb3a66bef79c9e9b0149fa7684d7b0"),
 "AEOS_项目开发执行手册_V1.0.docx": (48367, "9c93ad7b3b0a540506ae837f0d4381010b013abf7f46afa428014a5d6ba69535"),
 "AEOS_开发点检与进度表_V1.0.xlsx": (55114, "0bce8229ced21817a7e9e7588f897f4d6f5de5ac751e459aadd19627331150ec"),
 "AEOS_企业数据与智能中台_Data_Foundation_总体方案_V0.2_AEOS_V7.2.docx": (1580452, "871b02246d07c4f0909aa613d3f6e68fc8b0fa72e1bd6f15ab885d703ccc128f")
}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true", help="Exit 1 when files missing or mismatched")
    args=p.parse_args()
    errors=0
    for name,(size,sha) in EXPECTED.items():
        path=ROOT/"docs"/name
        if not path.is_file():
            print(f"NOT_READY MISSING {name}")
            errors+=1
            continue
        raw=path.read_bytes()
        actual=hashlib.sha256(raw).hexdigest()
        if len(raw)!=size or actual.lower()!=sha.lower():
            print(f"NOT_READY MISMATCH {name}: size={len(raw)}, sha256={actual}")
            errors+=1
        else:
            print(f"PASS {name}")
    print(f"BASELINE_READY={'false' if errors else 'true'}; checked={len(EXPECTED)}, failures={errors}")
    return 1 if errors and args.strict else 0
if __name__=="__main__":
    sys.exit(main())
