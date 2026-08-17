"""
Simple product generator that uses company.build_company_plan to create an ordered scaffold
per relevant department. This simulates teams producing artifacts in an ordered, non-conflicting
way. The generator writes small README files for each department in the project folder.

Usage: python scripts/generate_product.py --name sample_site --brief "fullstack website"
"""
import argparse
import os
import sys
import pathlib
# ensure repo root on sys.path so local package imports work when running as a script
_repo_root = str(pathlib.Path(__file__).resolve().parents[1])
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from company.selection import build_company_plan


def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def generate(name: str, brief: str, root: str = "projects"):
    project_root = os.path.join(root, name)
    os.makedirs(project_root, exist_ok=True)
    plan = build_company_plan({"name": name, "goals": brief})

    # top-level manifest
    write_file(
        os.path.join(project_root, "MANIFEST.json"),
        str(plan)
    )

    # create per-department simple artifacts in order
    for dept in plan["departments"]:
        key = dept["key"]
        dpath = os.path.join(project_root, key)
        os.makedirs(dpath, exist_ok=True)
        readme = f"# {dept['title']} ({dept['key']})\n\nOwner: {dept['manager']}\n\nScope: {dept['scope']}\n\nTasks:\n- Provide deliverables for the project brief.\n- Publish a machine-readable contract file to the project root (e.g., {key}.contract.json)\n"
        write_file(os.path.join(dpath, "README.md"), readme)
        # a minimal contract file other teams can read
        contract = {
            "team": key,
            "produces": ["api-spec.json"] if "api" in key or "backend" in key or "api_department" in key else ["artifact.txt"],
            "depends_on": []
        }
        write_file(os.path.join(project_root, f"{key}.contract.json"), str(contract))

    print("Generated project:", project_root)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--brief", required=True)
    args = p.parse_args()
    generate(args.name, args.brief)
