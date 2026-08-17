from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

@given(name=st.text(min_size=1, max_size=50), domain=st.text(min_size=1, max_size=20), stack=st.sampled_from(['fullstack','api','static']), goals=st.text(max_size=200))
def test_plan_random(name, domain, stack, goals):
    payload = {"name": name, "domain": domain, "goals": goals, "constraints": "", "stack": stack}
    r = client.post('/plan', json=payload)
    # should never 5xx
    assert r.status_code < 500
    # should return departments list
    j = r.json()
    assert 'departments' in j
    assert isinstance(j['departments'], list)
