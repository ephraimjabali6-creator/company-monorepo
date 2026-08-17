"""
Generate a deployable fullstack template (Next.js frontend scaffold + FastAPI backend) in projects/<name>-template.
This creates minimal files, Dockerfiles, and CI hints so the template can be used as a starting point.
"""
import os
import sys
import pathlib

_repo_root = str(pathlib.Path(__file__).resolve().parents[1])
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate(name: str, root: str = 'projects'):
    base = os.path.join(root, f"{name}-template")
    os.makedirs(base, exist_ok=True)

    # FastAPI backend
    backend = os.path.join(base, 'backend')
    write(os.path.join(backend, 'app.py'), """from fastapi import FastAPI
app=FastAPI()

# Expose a simple health endpoint and prometheus metrics when available
@app.get('/health')
def health():
    return {'status':'ok'}

# optional metrics mounting if prometheus_client is installed
try:
    from prometheus_client import make_asgi_app
    app.mount('/metrics', make_asgi_app())
except Exception:
    pass
""")
    write(os.path.join(backend, 'requirements.txt'), "fastapi\nuvicorn[standard]\nprometheus_client\n")
    write(os.path.join(backend, 'Dockerfile'), """FROM python:3.10-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]\n""")

    # Next.js frontend (minimal)
    frontend = os.path.join(base, 'frontend')
    write(os.path.join(frontend, 'package.json'), """{\n  \"name\": \"nextjs-app\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\"\n  }\n}\n""")
    write(os.path.join(frontend, 'pages', 'index.js'), """import {useEffect, useState} from 'react'
export default function Home(){
  const [status, setStatus] = useState('loading')
  useEffect(()=>{
    fetch(process.env.NEXT_PUBLIC_BACKEND_URL || '/api').then(r=>r.json()).then(j=>setStatus(j.status||'ok')).catch(()=>setStatus('unreachable'))
  },[])
  return <div style={{fontFamily:'sans-serif',padding:20}}><h1>Next.js App</h1><p>Backend status: {status}</p></div>
}
""")
    write(os.path.join(frontend, 'Dockerfile'), """FROM node:18-alpine\nWORKDIR /app\nCOPY package.json .\nRUN npm install --silent\nCOPY . .\nCMD ["npm","start"]\n""")

    # Top-level README
    write(os.path.join(base, 'README.md'), f"# Template {name}\n\nBackend: ./backend\nFrontend: ./frontend\n")
    print('Generated template at', base)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: generate_template.py <name>')
        sys.exit(1)
    generate(sys.argv[1])
