import requests
from requests.auth import HTTPBasicAuth
import os

# Load credentials from environment variables
WORKFLOW_TOKEN = os.getenv("WORKFLOW_TOKEN")
WORKFLOW_SECRET = os.getenv("WORKFLOW_SECRET")

response = requests.get(
    "https://sandbox.alloy.co/v1/parameters/",
    auth=HTTPBasicAuth(WORKFLOW_TOKEN, WORKFLOW_SECRET)
)

print(response.json())  # This might show workflow-related details
