import os
from jira import JIRA
from datetime import datetime, timezone

host = os.environ["JIRA_HOST"]
pat = os.environ["JIRA_PAT"]
issue_key = os.environ["JIRA_ISSUE_KEY"]

if not host:
    raise Exception("JIRA_HOST environment variable is not set")
if not pat:
    raise Exception("JIRA_PAT environment variable is not set")
if not issue_key:
    raise Exception("JIRA_ISSUE_KEY environment variable is not set")

headers = JIRA.DEFAULT_OPTIONS["headers"].copy()
headers["Authorization"] = f"Bearer {pat}"
jira = JIRA(server=host, options={"headers": headers})

# Log day
time_spent = "8h"

now = datetime.now(timezone.utc)
# skip if accidentally run this script on the weekend
if now.weekday() >= 5:
    raise Exception("It's weekend! No need to log work today.")
# todo add check for public holiday
# todo add check if the worklog is already logged
# todo add check for personal day off

start_time = now.replace(hour=7, minute=0, second=0, microsecond=0)

try:
    jira.add_worklog(issue=issue_key, timeSpent=time_spent, started=start_time)
except Exception as e:
    print(e)