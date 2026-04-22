import subprocess
import random
from datetime import datetime, timedelta
import os

# ─── Config ───────────────────────────
REPO_PATH = "."
DAYS = 30

# Realistic commit messages for cybersecurity projects
COMMIT_MESSAGES = [
    "fix threat parsing logic",
    "update feed aggregator",
    "improve dashboard UI",
    "add new threat indicators",
    "refactor alert system",
    "fix false positive detection",
    "update threat intelligence sources",
    "improve data visualization",
    "add IOC filtering",
    "fix API rate limiting",
    "update documentation",
    "add new detection rules",
    "improve performance",
    "fix data normalization",
    "add export functionality",
    "update dependencies",
    "fix XSS vulnerability",
    "improve threat scoring",
    "add dark web monitoring",
    "fix connection timeout",
    "refactor database queries",
    "add new threat categories",
    "improve search functionality",
    "fix memory leak",
    "update alert thresholds",
    "add logging functionality",
    "fix authentication bug",
    "improve error handling",
    "add new data sources",
    "update config files"
]

# Different file types to modify
FILES = [
    "README.md",
    "activity.log",
    "CHANGELOG.md",
    "notes.txt"
]

def make_commit(timestamp, message):
    # Pick random file to modify
    filename = random.choice(FILES)
    
    with open(filename, "a") as f:
        f.write(f"\n<!-- {timestamp} - {message} -->")
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = timestamp
    env["GIT_COMMITTER_DATE"] = timestamp
    
    subprocess.run(["git", "add", "."], cwd=REPO_PATH)
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=REPO_PATH,
        env=env
    )
    print(f"✅ {timestamp[:10]} → {message}")

# ─── Main Logic ───────────────────────
base = datetime.now()
total = 0

for i in range(DAYS):
    date = base - timedelta(days=i)
    weekday = date.weekday()
    
    # Realistic patterns
    rand = random.random()
    
    if weekday < 5:  # weekdays
        if rand < 0.15:
            num_commits = 0      # 15% chance no commits
        elif rand < 0.35:
            num_commits = 1      # 20% chance 1 commit
        elif rand < 0.60:
            num_commits = random.randint(2, 3)   # 25% chance 2-3
        elif rand < 0.80:
            num_commits = random.randint(3, 5)   # 20% chance 3-5
        else:
            num_commits = random.randint(6, 9)   # 20% burst day
    else:  # weekends
        if rand < 0.35:
            num_commits = 0      # 35% chance no commits
        elif rand < 0.65:
            num_commits = 1      # 30% chance 1 commit
        elif rand < 0.85:
            num_commits = random.randint(2, 3)   # 20% chance 2-3
        else:
            num_commits = random.randint(4, 6)   # 15% weekend grind

    # Spread commits across realistic hours
    used_times = set()
    for _ in range(num_commits):
        # Coding sessions: morning, afternoon, late night
        session = random.choice(["morning", "afternoon", "night"])
        if session == "morning":
            hour = random.randint(8, 11)
        elif session == "afternoon":
            hour = random.randint(13, 18)
        else:
            hour = random.randint(20, 23)
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        # Avoid duplicate timestamps
        while (hour, minute) in used_times:
            minute = random.randint(0, 59)
        used_times.add((hour, minute))
        
        timestamp = date.replace(
            hour=hour,
            minute=minute,
            second=second
        ).strftime("%Y-%m-%dT%H:%M:%S")
        
        message = random.choice(COMMIT_MESSAGES)
        make_commit(timestamp, message)
        total += 1

print(f"\n🎉 Done! {total} commits created")
print("Now run: git push origin main")