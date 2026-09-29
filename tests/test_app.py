import os
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"]="test-secret"

from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    r=client.get("/api/health")
    assert r.status_code==200
    assert r.json()["status"]=="ok"

def test_home_requires_login():
    c=TestClient(app)
    r=c.post("/api/generate-home",json={"budget":10000,"rooms":["Living Room"],"style":"Modern","notes":""})
    assert r.status_code==401
