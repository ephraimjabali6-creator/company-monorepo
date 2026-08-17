import os
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)


def test_missing_api_key():
    r = client.get('/gateway/echo')
    assert r.status_code == 401


def test_invalid_api_key():
    r = client.get('/gateway/echo', headers={'x-api-key': 'bad'})
    assert r.status_code == 403


def test_rate_limiting_and_valid_key(monkeypatch):
    # ensure a controlled API_KEYS env
    monkeypatch.setenv('API_KEYS', 'test-key')
    # call within limit
    for i in range(1, 6):
        r = client.get('/gateway/echo', headers={'x-api-key': 'test-key'})
        assert r.status_code == 200
    # exceed limit
    r = client.get('/gateway/echo', headers={'x-api-key': 'test-key'})
    assert r.status_code == 429
