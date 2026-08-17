from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from company.selection import build_company_plan
from services.api.gateway import router as gateway_router, attach_middleware as attach_gateway_middleware

# Prometheus metrics ASGI app
try:
    from prometheus_client import make_asgi_app
except Exception:
    make_asgi_app = None

app = FastAPI(title="Company Orchestration API")

# register the gateway router (API key, rate limiting) under /gateway
app.include_router(gateway_router, prefix="/gateway")
# attach the middleware to the app so requests are validated and rate-limited
try:
    attach_gateway_middleware(app)
except Exception:
    # safe fallback for test environments where redis or other optional deps may be absent
    pass

# mount prometheus metrics if available
if make_asgi_app is not None:
    app.mount('/metrics', make_asgi_app())


class Product(BaseModel):
    id: int
    name: str
    description: str = ""


class ProjectBrief(BaseModel):
    name: str = Field(..., min_length=1)
    domain: str = "general product"
    goals: str = ""
    constraints: str = ""
    stack: str = "fullstack"


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok"}


@app.get("/departments")
def departments() -> dict[str, Any]:
    return {
        "departments": [
            "ceo",
            "cto",
            "product_management",
            "frontend_engineering",
            "backend_engineering",
            "api_department",
            "security_team",
            "devops",
            "qa",
        ]
    }


@app.get('/status')
def status() -> dict[str, Any]:
    """Return machine-readable project and department status overview."""
    import os
    projects = []
    root = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'projects')
    root = os.path.abspath(root)
    if not os.path.exists(root):
        return {"projects": []}
    for name in sorted(os.listdir(root)):
        pdir = os.path.join(root, name)
        if not os.path.isdir(pdir):
            continue
        # list contract files as produced by teams
        contracts = [f for f in os.listdir(pdir) if f.endswith('.contract.json')]
        projects.append({"name": name, "contracts": contracts})
    return {"projects": projects}


@app.get('/logs')
def logs(n: int = 50):
    from services.api.logger import recent
    return {"logs": recent(n)}


@app.post("/plan")
def plan_project(payload: ProjectBrief) -> dict[str, Any]:
    plan = build_company_plan({
        "name": payload.name,
        "domain": payload.domain,
        "goals": payload.goals,
        "constraints": payload.constraints,
        "stack": payload.stack,
    })
    return {
        "project": payload.name,
        "summary": plan["summary"],
        "departments": plan["departments"],
    }


@app.post("/product")
def create_product(p: Product):
    return {"created": True, "product": p.model_dump()}
