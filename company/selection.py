from __future__ import annotations

from typing import Any, Iterable

from .department_registry import DEPARTMENTS, ORDERED_DEPARTMENTS


DEFAULT_REQUIRED = ["ceo", "cto", "product_management", "engineering", "qa", "devops", "api_department"]


def _normalize(value: str) -> str:
    return " ".join(value.lower().replace("-", " ").replace("_", " ").split())


def _contains_any(text: str, phrases: Iterable[str]) -> bool:
    normalized = _normalize(text)
    return any(phrase in normalized for phrase in [_normalize(p) for p in phrases])


def select_departments(spec: str | dict[str, Any]) -> list[str]:
    if isinstance(spec, dict):
        text = " ".join(str(v) for v in spec.values())
    else:
        text = str(spec)

    keywords = _normalize(text)
    selected = set(DEFAULT_REQUIRED)

    if _contains_any(keywords, ["website", "web app", "landing page", "marketing site", "saas", "frontend"]) or "ui" in keywords:
        selected.update(["frontend_engineering", "ux_ui", "design_systems", "seo", "product_management"])
    if _contains_any(keywords, ["mobile app", "android", "ios", "react native", "flutter"]):
        selected.update(["mobile_engineering", "ux_ui", "qa"])
    if _contains_any(keywords, ["desktop", "native app", "electron", "tauri", "windows", "mac", "linux"]):
        selected.update(["desktop_engineering", "devops", "qa"])
    if _contains_any(keywords, ["api", "backend", "database", "service", "microservice", "fullstack", "system"]) or "backend" in keywords:
        selected.update(["backend_engineering", "api_department", "cloud_infra", "sre", "devops"])
    if _contains_any(keywords, ["ai", "ml", "model", "agent", "intelligent", "llm", "recommendation"]) or "intelligent" in keywords:
        selected.update(["ml_ai", "data_analytics", "optimization", "security_team"])
    if _contains_any(keywords, ["security", "cyber", "bank", "finance", "health", "patient", "compliance", "encryption", "identity"]):
        selected.update(["security_team", "encryption_engineering", "cybersecurity", "blue_team", "red_team", "legal_compliance", "cso"])
    if _contains_any(keywords, ["design", "brand", "visual", "3d", "4d", "aesthetic", "creative"]):
        selected.update(["aesthetic_design", "design_systems", "ux_ui"])
    if _contains_any(keywords, ["sre", "reliability", "uptime", "monitoring", "observability"]):
        selected.update(["sre", "devops", "cloud_infra"])
    if _contains_any(keywords, ["marketing", "growth", "campaign", "seo", "acquisition", "brand"]):
        selected.update(["cmo", "seo", "product_management"])
    if _contains_any(keywords, ["legal", "privacy", "gdpr", "hipaa", "contract", "compliance"]):
        selected.update(["legal_compliance", "clo"])
    if _contains_any(keywords, ["data", "analytics", "dashboard", "reporting", "warehouse", "etl"]):
        selected.update(["data_analytics", "cdo"])
    if _contains_any(keywords, ["business", "operations", "organization", "enterprise"]):
        selected.update(["coo", "cao", "cfo", "hr"])

    selected.add("cto")
    selected.add("ceo")
    selected.add("product_management")
    selected.add("engineering")
    selected.add("qa")

    ordered = []
    for key in ORDERED_DEPARTMENTS:
        if key in selected:
            ordered.append(key)
    return ordered


def build_company_plan(spec: str | dict[str, Any]) -> dict[str, Any]:
    selected = select_departments(spec)
    departments = [DEPARTMENTS[key] for key in selected if key in DEPARTMENTS]

    return {
        "departments": [
            {
                "key": dept.key,
                "title": dept.title,
                "manager": dept.manager,
                "scope": dept.scope,
                "tags": list(dept.tags),
            }
            for dept in departments
        ],
        "summary": "Relevant departments only. Irrelevant teams are intentionally excluded to reduce drift, confusion, and coordination overhead.",
    }
