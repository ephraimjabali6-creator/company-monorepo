from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class Department:
    key: str
    title: str
    manager: str
    scope: str
    tags: Tuple[str, ...] = field(default_factory=tuple)


DEPARTMENTS: dict[str, Department] = {
    "ceo": Department("ceo", "CEO", "Chief Executive Officer", "Strategy, prioritization, executive alignment", ("strategy", "leadership", "vision")),
    "cfo": Department("cfo", "CFO", "Chief Financial Officer", "Budgeting, ROI, commercial viability", ("finance", "budget", "roi")),
    "cto": Department("cto", "CTO", "Chief Technology Officer", "Architecture, platform standards, technical decisions", ("technology", "architecture", "standards")),
    "coo": Department("coo", "COO", "Chief Operating Officer", "Operations and delivery execution", ("operations", "delivery", "process")),
    "cao": Department("cao", "CAO", "Chief Administrative Officer", "Administrative systems, governance and office operations", ("admin", "governance", "operations")),
    "cso": Department("cso", "CSO", "Chief Security Officer", "Security governance and risk management", ("security", "risk", "governance")),
    "chro": Department("chro", "CHRO", "Chief Human Resources Officer", "Human capital, hiring, culture, org health", ("hr", "people", "culture")),
    "cmo": Department("cmo", "CMO", "Chief Marketing Officer", "Brand, acquisition, campaigns, messaging", ("marketing", "growth", "brand")),
    "cco": Department("cco", "CCO", "Chief Customer Officer", "Customer success and delivery confidence", ("customer", "success", "support")),
    "cio": Department("cio", "CIO", "Chief Information Officer", "Systems, IT governance and support", ("it", "infrastructure", "systems")),
    "cdo": Department("cdo", "CDO", "Chief Data Officer", "Data strategy, data product and governance", ("data", "analytics", "governance")),
    "cpo": Department("cpo", "CPO", "Chief Product Officer", "Product direction, roadmap and release fit", ("product", "roadmap", "strategy")),
    "clo": Department("clo", "CLO", "Chief Legal Officer", "Legal, contracts, compliance and regulatory issues", ("legal", "compliance", "regulation")),
    "cro": Department("cro", "CRO", "Chief Revenue Officer", "Sales enablement and revenue operations", ("revenue", "sales", "growth")),
    "product_management": Department("product_management", "Product Management", "Product Manager", "Requirements translation, backlog ownership, prioritization", ("product", "planning", "backlog")),
    "frontend_engineering": Department("frontend_engineering", "Frontend Engineering", "Frontend Lead", "Web UI, interfaces, accessibility, web performance", ("frontend", "ui", "web")),
    "backend_engineering": Department("backend_engineering", "Backend Engineering", "Backend Lead", "Domain logic, integrations, persistence, service architecture", ("backend", "services", "platform")),
    "api_department": Department("api_department", "API Department", "API Platform Lead", "Public/private API contracts, auth, versioning, gateways, service integration", ("api", "gateway", "contracts")),
    "mobile_engineering": Department("mobile_engineering", "Mobile Engineering", "Mobile Lead", "Android/iOS/mobile app architecture and release", ("mobile", "ios", "android")),
    "desktop_engineering": Department("desktop_engineering", "Desktop Engineering", "Desktop Lead", "Native desktop, productivity tooling, installers", ("desktop", "native", "electron")),
    "design_systems": Department("design_systems", "Design Systems", "Design Lead", "Component libraries, UI standards, design tokens", ("design", "ux", "system")),
    "ux_ui": Department("ux_ui", "UX / UI", "UX Lead", "UX flows, information architecture, usability", ("ux", "ui", "research")),
    "aesthetic_design": Department("aesthetic_design", "Aesthetic Design", "Creative Director", "Brand identity, visual polish, 3D/4D product design", ("visual", "brand", "aesthetic")),
    "qa": Department("qa", "Quality Assurance", "QA Lead", "Regression, release validation, test strategy", ("testing", "quality", "qa")),
    "security_team": Department("security_team", "Security Team", "Security Director", "Security planning, threat modeling, controls", ("security", "controls", "threats")),
    "encryption_engineering": Department("encryption_engineering", "Encryption Engineering", "Encryption Lead", "Key handling, cipher selection, secure storage", ("encryption", "keys", "crypto")),
    "cybersecurity": Department("cybersecurity", "Cybersecurity", "Cybersecurity Lead", "Monitoring, defense, incident processing", ("cyber", "monitoring", "defense")),
    "blue_team": Department("blue_team", "Blue Team", "Blue Team Lead", "Defensive monitoring, alerts and detection", ("blue", "defense", "detection")),
    "red_team": Department("red_team", "Red Team", "Red Team Lead", "Offense simulation, exploit testing, adversarial exercises", ("red", "pentest", "adversarial")),
    "devops": Department("devops", "DevOps", "DevOps Lead", "CI/CD, environments, automation and deployment", ("devops", "ci", "cd")),
    "cloud_infra": Department("cloud_infra", "Cloud Infrastructure", "Cloud Lead", "Platform services, scaling, cloud resources", ("cloud", "infra", "platform")),
    "sre": Department("sre", "SRE", "Site Reliability Engineer", "Reliability, observability, incident response", ("sre", "reliability", "ops")),
    "data_analytics": Department("data_analytics", "Data & Analytics", "Data Lead", "Analytics, insights, instrumentation, experimentation", ("data", "analytics", "dashboards")),
    "ml_ai": Department("ml_ai", "ML & AI", "AI Lead", "Intelligent systems, models, agentic workflows", ("ai", "ml", "intelligence")),
    "seo": Department("seo", "SEO", "SEO Lead", "Search performance, discovery and traffic optimization", ("seo", "search", "discovery")),
    "it_support": Department("it_support", "IT Support", "IT Lead", "Internal tooling, endpoint support, environment help", ("it", "support", "helpdesk")),
    "hr": Department("hr", "HR", "HR Manager", "People operations, hiring and retention", ("hr", "people", "recruiting")),
    "legal_compliance": Department("legal_compliance", "Legal & Compliance", "Legal Lead", "Privacy, contracts and regulatory readiness", ("legal", "compliance", "privacy")),
    "optimization": Department("optimization", "Optimization Team", "Optimization Lead", "Performance, cost and efficiency tuning across the stack", ("optimization", "efficiency", "benchmarking")),
    "engineering": Department("engineering", "Engineering", "Engineering Manager", "Core software delivery across product squads", ("engineering", "delivery", "build")),
}

ORDERED_DEPARTMENTS = [
    "ceo", "cfo", "cto", "coo", "cso", "chro", "cmo", "cco", "cio", "cdo", "cpo", "clo", "cro",
    "product_management", "frontend_engineering", "backend_engineering", "api_department", "mobile_engineering", "desktop_engineering",
    "design_systems", "ux_ui", "aesthetic_design", "qa", "security_team", "encryption_engineering",
    "cybersecurity", "blue_team", "red_team", "devops", "cloud_infra", "sre", "data_analytics", "ml_ai",
    "seo", "it_support", "hr", "legal_compliance", "optimization", "engineering"
]
