import requests

ORG = "Overby-Industries"
API = f"https://api.github.com/orgs/{ORG}/repos?per_page=100&type=public"

resp = requests.get(API)
repos = resp.json()

table = "| Repo | Description | Stars | Issues | PRs | Contributors | Last Commit |\n"
table += "|------|-------------|-------|--------|-----|--------------|-------------|\n"

for repo in sorted(repos, key=lambda r: r["name"].lower()):
    name = repo["name"]
    desc = repo["description"] or ""
    url = repo["html_url"]

    stars_badge = f"![Stars](https://img.shields.io/github/stars/{ORG}/{name}?style=social)"
    issues_badge = f"![Issues](https://img.shields.io/github/issues-raw/{ORG}/{name})"
    prs_badge = f"![PRs](https://img.shields.io/github/issues-pr-raw/{ORG}/{name})"
    contrib_badge = f"![Contrib](https://img.shields.io/github/contributors/{ORG}/{name})"
    commit_badge = f"![Commit](https://img.shields.io/github/last-commit/{ORG}/{name})"

    table += f"| [{name}]({url}) | {desc} | {stars_badge} | {issues_badge} | {prs_badge} | {contrib_badge} | {commit_badge} |\n"

# Inject into README.md between markers
with open("README.md") as f:
    text = f.read()

start = text.find("<!-- REPO_DASHBOARD_START -->")
end = text.find("<!-- REPO_DASHBOARD_END -->")

new_section = f"<!-- REPO_DASHBOARD_START -->\n{table}<!-- REPO_DASHBOARD_END -->"
if start != -1 and end != -1:
    updated = text[:start] + new_section + text[end+len("<!-- REPO_DASHBOARD_END -->"):]
else:
    updated = text + "\n\n" + new_section

with open("README.md", "w") as f:
    f.write(updated)
