import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WORKFLOW_TOKEN = os.getenv("WORKFLOW_TOKEN")
WORKFLOW_SECRET = os.getenv("WORKFLOW_SECRET")
PARAMETERS_ENDPOINT = "https://sandbox.alloy.co/v1/parameters/"

def get_required_parameters():
    """Fetches required fields from the Alloy API parameters endpoint."""
    response = requests.get(PARAMETERS_ENDPOINT, auth=(WORKFLOW_TOKEN, 
WORKFLOW_SECRET))
    
    if response.status_code == 200:
        parameters = response.json()
        print("Required Fields:", parameters.get("required", []))
        print("Optional Fields:", parameters.get("optional", []))
    else:
        print("Error fetching parameters:", response.status_code, 
response.text)

# Run the function when executing the script
if __name__ == "__main__":
    get_required_parameters()
