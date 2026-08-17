"""Validate per-project team contract JSON files produced by generators.
Usage: python scripts/validate_contracts.py [projects_dir]
"""
import json
import os
import sys


def validate_contract(path: str) -> bool:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
    except Exception as e:
        print(f"INVALID JSON {path}: {e}")
        return False
    # basic schema checks
    required = ['team', 'version']
    for k in required:
        if k not in j:
            print(f"Missing key {k} in {path}")
            return False
    return True


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else 'projects'
    if not os.path.exists(root):
        print('No projects directory, nothing to validate')
        return 0
    ok = True
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name)
        if not os.path.isdir(p):
            continue
        for f in os.listdir(p):
            if f.endswith('.contract.json'):
                path = os.path.join(p, f)
                if not validate_contract(path):
                    ok = False
    if not ok:
        print('One or more contracts invalid')
        sys.exit(2)
    print('All contracts valid')

if __name__ == '__main__':
    main()
