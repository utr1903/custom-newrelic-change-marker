import os
from datetime import datetime, timedelta
import json
import requests

# Parse env vars
newrelicAccountId = str(os.getenv("NEWRELIC_ACCOUNT_ID"))
newrelicLicenseKey = str(os.getenv("NEWRELIC_LICENSE_KEY"))
githubActor = str(os.getenv("GITHUB_ACTOR"))
githubJobId = str(os.getenv("GITHUB_JOB"))
githubRepository = str(os.getenv("GITHUB_REPOSITORY"))
githubRunId = str(os.getenv("GITHUB_RUN_ID"))
githubRunAttempt = str(os.getenv("GITHUB_RUN_ATTEMPT"))
githubRunnerName = str(os.getenv("RUNNER_NAME"))
githubRunnerOs = str(os.getenv("RUNNER_OS"))

startTimestamp = int(os.getenv("START_TIMESTAMP"))
# customEventName = str(os.getenv("CUSTOM_EVENT_NAME"))
customEventName = "MyTestEvent"

# Decide the New Relic events endpoint
newrelicEventsEndpoint = f"https://insights-collector.eu01.nr-data.net/v1/accounts/${newrelicAccountId}/events" if newrelicLicenseKey[:2] == "eu" else f"https://insights-collector.nr-data.net/v1/accounts/${newrelicAccountId}/events"

# Prepare request headers
headers = {
    "Content-Type": "application/json",
    "Api-Key": newrelicLicenseKey,
}

endTimestamp = datetime.now().timestamp()

# Prepare custom event
data = [{
    "eventType": customEventName,
    "githubActor": githubActor,
    "githubJobId": githubJobId,
    "githubRepository": githubRepository,
    "githubRunId": githubRunId,
    "githubRunAttempt": githubRunAttempt,
    "githubRunnerName": githubRunnerName,
    "githubRunnerOs": githubRunnerOs,
    "startTimestamp": startTimestamp,
    "endTimestamp": endTimestamp,
    "duration": endTimestamp - startTimestamp,
}]

# Make POST request to create custom event
response = requests.post(newrelicEventsEndpoint,
                         data=json.dumps(data), headers=headers)

# Checking the response status
print(response.status_code)
if response.status_code == 200:
    print("Creating custom event succeeded.")
    exit(0)
else:
    print(f"Creating custom event failed: {response.text}")
    exit(1)
