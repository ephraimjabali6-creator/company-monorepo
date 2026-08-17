from services.api.main import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


def test_status_empty():
    # ensure projects folder exists but empty
    import pathlib
    repo_root = pathlib.Path(__file__).resolve().parents[3]
    root = repo_root.joinpath('projects')
    if root.exists():
        # remove generated sample if present
        import shutil
        shutil.rmtree(root)
    r = client.get('/status')
    assert r.status_code == 200
    assert r.json() == {"projects": []}


def test_logs_endpoint():
    r = client.get('/logs')
    assert r.status_code == 200
    assert 'logs' in r.json()
