import os
from datetime import datetime, timedelta
import json
import requests

# Parse env vars
newrelicAccountId = str(os.getenv("NEWRELIC_ACCOUNT_ID"))
newrelicLicenseKey = str(os.getenv("NEWRELIC_LICENSE_KEY"))
# customEventName = str(os.getenv("CUSTOM_EVENT_NAME"))
customEventName = "MyTestEvent"

# Decide the New Relic events endpoint
newrelicEventsEndpoint = f"https://insights-collector.eu01.nr-data.net/v1/accounts/${
    newrelicAccountId}/events" if newrelicLicenseKey[:2] == "eu" else f"https://insights-collector.nr-data.net/v1/accounts/${newrelicAccountId}/events"

# Prepare request headers
headers = {
    "Content-Type": "application/json",
    "Api-Key": newrelicLicenseKey,
}

endTime = datetime.now()
startTime = endTime - timedelta(minutes=1)

# Prepare custom event
data = [{
    "eventType": customEventName,
    "startTimestamp": startTime.timestamp(),
    "endTimestamp": endTime.timestamp(),
    "duration": endTime.timestamp() - startTime.timestamp(),
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
