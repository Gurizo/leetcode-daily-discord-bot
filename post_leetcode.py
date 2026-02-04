import os

import requests

WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]

QUERY = """
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


def main() -> None:
    res = requests.post(
        "https://leetcode.com/graphql",
        json={"query": QUERY},
        headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"},
        timeout=30,
    )
    res.raise_for_status()

    payload = res.json()
    data = payload["data"]["activeDailyCodingChallengeQuestion"]

    title = data["question"]["title"]
    difficulty = data["question"]["difficulty"]
    link = "https://leetcode.com" + data["link"]
    date = data["date"]

    msg = f"🧠 **LeetCode Daily ({date})**\n**{title}** ({difficulty})\n{link}"

    r = requests.post(WEBHOOK, json={"content": msg}, timeout=30)
    r.raise_for_status()


if __name__ == "__main__":
    main()
