from company.selection import build_company_plan, select_departments


def test_select_departments_web_app():
    plan = select_departments("build a SaaS website with dashboard and SEO")
    assert "frontend_engineering" in plan
    assert "backend_engineering" in plan or "seo" in plan
    assert "ceo" in plan


def test_build_company_plan_security_focus():
    plan = build_company_plan({
        "name": "Secure fintech product",
        "description": "Web app with encryption and compliance",
    })
    keys = {d["key"] for d in plan["departments"]}
    assert "security_team" in keys
    assert "legal_compliance" in keys
    assert "encryption_engineering" in keys
    assert "frontend_engineering" in keys
