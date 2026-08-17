from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_create_product():
    r = client.post('/product', json={"id":1, "name":"X"})
    assert r.status_code == 200
    d = r.json()
    assert d['created'] is True
    assert d['product']['name'] == 'X'
