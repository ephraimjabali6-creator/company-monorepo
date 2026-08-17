"""Simple orchestration runner: runs generate_product.py then validates contracts.
"""
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(__file__))

def run_generate(name='sample'):
    cmd = [sys.executable, os.path.join(ROOT,'scripts','generate_product.py'), name]
    subprocess.check_call(cmd)

def validate():
    cmd = [sys.executable, os.path.join(ROOT,'scripts','validate_contracts.py')]
    subprocess.check_call(cmd)

if __name__ == '__main__':
    run_generate('orchestrated-sample')
    validate()
    print('orchestration complete')
