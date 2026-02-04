cat > post_leetcode.py <<'PY'
import os
import requests

WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]

query = """
query questionOfToday {
  activeDailyCodingChallengeQuestion {
    date
    link
    question {
      title
      difficulty
      titleSlug
    }
  }
}
"""

res = requests.post(
    "https://leetcode.com/graphql",
    json={"query": query},
    headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"},
    timeout=30,
)
res.raise_for_status()

data = res.json()["data"]["activeDailyCodingChallengeQuestion"]
title = data["question"]["title"]
difficulty = data["question"]["difficulty"]
link = "https://leetcode.com" + data["link"]
date = data["date"]

msg = f"🧠 **LeetCode Daily ({date})**\n**{title}** ({difficulty})\n{link}"

r = requests.post(WEBHOOK, json={"content": msg}, timeout=30)
r.raise_for_status()
PY
