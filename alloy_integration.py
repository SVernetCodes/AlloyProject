import os
import requests
import re
import getpass # Used to mask SSN input
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials securely
WORKFLOW_TOKEN = os.getenv( "WORKFLOW_TOKEN" )
WORKFLOW_SECRET = os.getenv( "WORKFLOW_SECRET" )
EVALUATIONS_ENDPOINT = "https://sandbox.alloy.co/v1/evaluations/"

# Ensure API credentials are loaded
if not WORKFLOW_TOKEN or not WORKFLOW_SECRET:
    raise ValueError( "API credentials are missing. Please check your .env file." )

# List of valid U.S. state abbreviations
VALID_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
    "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

def get_required_parameters():
    """Fetches required fields from the Alloy API parameters endpoint."""
    response = requests.get("https://sandbox.alloy.co/v1/parameters/",
                            auth=(WORKFLOW_TOKEN, WORKFLOW_SECRET))

    if response.status_code == 200:
        parameters = response.json()
        print("Required Fields:", parameters.get("required", []))
        print("Optional Fields:", parameters.get("optional", []))
    else:
        print("Error fetching parameters:", response.status_code, response.text)

# Validation functions
def get_valid_name(prompt):
    """ Ensures name contains only alphabetical characters and is at least 2 characters"""
    while True:
        name = input(prompt).strip()
        if name.isalpha() and len(name) >= 2:
            return name
        print("Error: Name must contain only letters and be at least 2 characters long.")

def get_valid_state():
    while True:
        state = input("State (2-letter code, e.g., NY): ").strip().upper()
        if state in VALID_STATES:
            return state
        print("Error: Enter a valid U.S. state abbreviation.")

def get_valid_country():
    while True:
        country = input("Country (must be US): ").strip().upper()
        if country == "US":
            return country
        print("Error: Country must be 'US'.")

def get_valid_ssn():
    while True:
        ssn = input("SSN (9 digits, no dashes): ").strip()
        if ssn.isdigit() and len(ssn) == 9:
            return ssn
        print("Error: SSN must be exactly 9 digits.")

def get_valid_zip():
    while True:
        zip_code = input("ZIP Code (5 digits): ").strip()
        if zip_code.isdigit() and len(zip_code) == 5:
            return zip_code
        print("Error: ZIP Code must be exactly 5 digits.")

def get_valid_email():
    while True:
        email = input("Email Address: ").strip()
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            return email
        print("Error: Please enter a valid email address.")

# Function to get applicant details
def get_applicant_details():
    print("Enter applicant details:")
    applicant = {
        "name_first": get_valid_name("First Name: "),
        "name_last": get_valid_name("Last Name: "),
        "birth_date": input("Date of Birth (YYYY-MM-DD): ").strip(),
        "ssn": get_valid_ssn(),
        "email": get_valid_email(),
        "address_line_1": input("Address Line 1: ").strip(),
        "address_line_2": input("Address Line 2 (optional): ").strip(),
        "address_city": input("City: ").strip(),
        "address_state": get_valid_state(),
        "address_postal_code": get_valid_zip(),
        "address_country": get_valid_country()
    }
    return applicant
  
# Function to submit application
def submit_application(applicant_data):
    """Submits an application to Alloy's evaluation endpoint."""
    payload = {
        "name": "default",  # Update if Alloy provides a specific workflow name
        "attributes": applicant_data
    }

    response = requests.post(
        "https://sandbox.alloy.co/v1/evaluations/",
        auth=(WORKFLOW_TOKEN, WORKFLOW_SECRET),
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Function to process API response
def process_response(response):She
    """Processes API response and prints an appropriate message."""
    if not response:
        print("Error: No response received.")
        return

    print("\nFull API Response:\n", response, "\n")

    if "summary" in response:
        outcome = response["summary"].get("outcome", "Unknown")
        if outcome == "Approved":
            print("Congratulations! You are approved.")
        elif outcome == "Manual Review":
            print("Your application is under review. Please wait for updates.")
        elif outcome == "Deny":
            print("Unfortunately, we cannot approve your application at this time.")
        else:
            print("Unexpected response outcome:", outcome)
    else:
        print("API response does not contain 'summary'. Checking for possible issues...")
        if "error" in response and response["error"]:
            print(f"API Error: {response['error']}")
        elif "status_code" in response:
            print(f"API Status Code: {response['status_code']}")
            if response["status_code"] != 200:
                print("API returned a non-successful status. Please check credentials or request format.")
        else:
            print("Unknown API response structure. Please review the full response above.")

# Main function
def main():
    print("Welcome to Alloy API Integration")
    applicant_details = get_applicant_details()
    response = submit_application(applicant_details)
    process_response(response)

if __name__ == "__main__":
    main()
