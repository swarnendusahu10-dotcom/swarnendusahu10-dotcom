"""Fetch live GitHub data into data/*.json (profile, PR counts, contributions).

Uses GITHUB_TOKEN when present (CI) to avoid the anonymous rate limit.
The contributions calendar is read from the public contributions page.
"""
import json
import os
import re
from collections import Counter, defaultdict
from datetime import date

import requests
from bs4 import BeautifulSoup

USERNAME = "swarnendusahu10-dotcom"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com"


def save(name, obj):
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def fetch_profile(s):
    try:
        user = s.get(f"{API}/users/{USERNAME}", timeout=30).json()
        repos = s.get(f"{API}/users/{USERNAME}/repos",
                      params={"per_page": 100, "type": "owner"}, timeout=30).json()
        langs = Counter()
        for r in repos:
            if isinstance(r, dict) and not r.get("fork"):
                resp = s.get(r.get("languages_url", ""), timeout=30)
                if resp.ok:
                    langs.update(resp.json())
        save("profile.json", {
            "name": user.get("name") or "Swarnendu Sahu",
            "username": USERNAME,
            "created_at": user.get("created_at"),
            "public_repos": user.get("public_repos", len(repos) if isinstance(repos, list) else 8),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
            "stars": sum(r.get("stargazers_count", 0) for r in repos) if isinstance(repos, list) else 0,
            "languages": dict(langs.most_common()),
        })
        print("profile.json saved")
    except Exception as e:
        print("fetch_profile error:", e)


def fetch_counts(s):
    def total(q):
        try:
            r = s.get(f"{API}/search/issues", params={"q": q}, timeout=30)
            if r.ok:
                return r.json().get("total_count", 0)
        except Exception:
            pass
        return 0

    save("github.json", {
        "prs_opened": total(f"author:{USERNAME} type:pr"),
        "prs_merged": total(f"author:{USERNAME} type:pr is:merged"),
        "prs_open": total(f"author:{USERNAME} type:pr is:open"),
        "issues_opened": total(f"author:{USERNAME} type:issue"),
        "prs_reviewed": total(f"reviewed-by:{USERNAME} type:pr"),
    })
    print("github.json saved")


def fetch_contributions():
    html = requests.get(f"https://github.com/users/{USERNAME}/contributions",
                        headers={"User-Agent": "profile-art"}, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    tips = {}
    for tip in soup.find_all("tool-tip"):
        m = re.match(r"\s*(\d[\d,]*) contributions?", tip.get_text())
        tips[tip.get("for")] = int(m.group(1).replace(",", "")) if m else 0
    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append({
            "date": cell["data-date"],
            "level": int(cell.get("data-level", 0)),
            "count": tips.get(cell.get("id"), 0),
        })
    if not days:
        print("Warning: No contribution cells found; using empty days list")
        days = [{"date": date.today().isoformat(), "level": 0, "count": 0}]

    days.sort(key=lambda d: d["date"])
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1
    best = max(days, key=lambda d: d["count"])
    monthly = defaultdict(int)
    weekday = Counter()
    for d in days:
        monthly[d["date"][:7]] += d["count"]
        weekday[date.fromisoformat(d["date"]).strftime("%A")] += d["count"]

    save("contributions.json", {
        "username": USERNAME,
        "days": days,
        "stats": {
            "total": sum(counts),
            "current_streak": current,
            "longest_streak": longest,
            "best_day": {"date": best["date"], "count": best["count"]},
            "active_days": sum(1 for c in counts if c),
            "busiest_weekday": weekday.most_common(1)[0][0] if sum(counts) else "-",
            "monthly": dict(monthly),
            "range": [days[0]["date"], days[-1]["date"]],
        },
    })
    print("contributions.json saved")


def fetch_activity(s):
    """Category counts + top merged-PR repos for the GitHub activity card."""
    path = os.path.join(ROOT, "data", "activity.json")
    act = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                act = json.load(f)
        except Exception:
            pass

    def total(q):
        try:
            r = s.get(f"{API}/search/issues", params={"q": q}, timeout=30)
            if r.ok:
                return r.json().get("total_count", 0)
        except Exception:
            pass
        return 0

    repos = []
    candidate_repos = [
        ("RocketChat/EmbeddedChat", "EmbeddedChat"),
        (f"{USERNAME}/AI-DETECTION", "AI-DETECTION"),
        (f"{USERNAME}/FoodDeliveryPrediction", "FoodDelivery"),
        (f"{USERNAME}/StockLite", "StockLite"),
        (f"{USERNAME}/EmbeddedChat", "EmbeddedChat-fork"),
    ]
    for repo, label in candidate_repos:
        n = total(f"author:{USERNAME} repo:{repo}")
        if n:
            repos.append([label, n])
    repos.sort(key=lambda r: -r[1])
    if repos:
        act["repos"] = repos[:6]

    try:
        from datetime import timedelta
        end = date.today()
        start = end - timedelta(days=365)
        query = {"query": "query($u:String!,$from:DateTime!,$to:DateTime!)"
                 "{user(login:$u){contributionsCollection(from:$from,to:$to)"
                 "{totalCommitContributions totalPullRequestContributions "
                 "totalIssueContributions totalPullRequestReviewContributions}}}",
                 "variables": {"u": USERNAME,
                               "from": f"{start.isoformat()}T00:00:00Z",
                               "to": f"{end.isoformat()}T23:59:59Z"}}
        r = s.post("https://api.github.com/graphql", json=query, timeout=30)
        if r.ok:
            data = r.json().get("data", {})
            if data and data.get("user"):
                cc = data["user"]["contributionsCollection"]
                act.update({"commits": cc.get("totalCommitContributions", 0),
                            "pull_requests": cc.get("totalPullRequestContributions", 0),
                            "issues": cc.get("totalIssueContributions", 0),
                            "reviews": cc.get("totalPullRequestReviewContributions", 0)})
    except Exception as e:
        print("activity graphql skipped:", e)

    # Defaults if token not present or graphql unavailable
    c_data = {}
    c_path = os.path.join(ROOT, "data", "contributions.json")
    if os.path.exists(c_path):
        with open(c_path, encoding="utf-8") as f:
            c_data = json.load(f).get("stats", {})

    total_contribs = c_data.get("total", 0)
    if "commits" not in act or not act.get("commits"):
        # Estimate breakdown from contributions
        act.setdefault("commits", max(total_contribs - 14, 0))
        act.setdefault("pull_requests", 14)
        act.setdefault("issues", 0)
        act.setdefault("reviews", 0)

    save("activity.json", act)
    print("activity.json saved")


def main():
    s = requests.Session()
    s.headers["Accept"] = "application/vnd.github+json"
    if os.environ.get("GITHUB_TOKEN"):
        s.headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    fetch_profile(s)
    fetch_counts(s)
    fetch_contributions()
    fetch_activity(s)


if __name__ == "__main__":
    main()
