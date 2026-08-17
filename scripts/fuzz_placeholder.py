"""Lightweight fuzzing placeholder — runable in CI. Replace with true fuzz harness later.
"""
import random
import requests

BASE = 'http://localhost:8000'

def random_brief():
    names = ['alpha', 'beta', 'gamma']
    return {
        'name': random.choice(names) + '-' + str(random.randint(1,1000)),
        'domain': random.choice(['web','mobile','iot']),
        'goals': '',
        'constraints': '',
        'stack': random.choice(['fullstack','api','static'])
    }

if __name__ == '__main__':
    # try pinging backend; if not available, skip (CI will run after docker stack if desired)
    try:
        r = requests.get(BASE + '/health', timeout=2)
        if r.status_code != 200:
            print('backend unreachable, skipping fuzz')
        else:
            for i in range(5):
                b = random_brief()
                r = requests.post(BASE + '/plan', json=b, timeout=3)
                print('fuzz', i, r.status_code)
    except Exception as e:
        print('skip fuzz:', e)
