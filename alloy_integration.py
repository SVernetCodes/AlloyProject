import requests
import re

# Placeholder for API credentials
WORKFLOW_TOKEN = "your_workflow_token"
WORKFLOW_SECRET = "your_workflow_secret"
EVALUATIONS_ENDPOINT = "https://sandbox.alloy.co/v1/evaluations/"

# List of valid U.S. state abbreviations
VALID_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
    "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# Validation functions
def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        if len(name) >= 2:
            return name
        print("Error: Name must be at least 2 characters long.")

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
    response = requests.post(
        EVALUATIONS_ENDPOINT,
        auth=(WORKFLOW_TOKEN, WORKFLOW_SECRET),
        json={"applicant": applicant_data}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Function to process API response
def process_response(response):
    if response and "summary" in response:
        outcome = response["summary"].get("outcome", "Unknown")
        if outcome == "Approved":
            print("Congratulations! You are approved.")
        elif outcome == "Manual Review":
            print("Your application is under review. Please wait for updates.")
        elif outcome == "Deny":
            print("Unfortunately, we cannot approve your application at this time.")
        else:
            print("Unexpected response:", response)
    else:
        print("Error: Invalid response received.")

# Main function
def main():
    print("Welcome to Alloy API Integration")
    applicant_details = get_applicant_details()
    response = submit_application(applicant_details)
    process_response(response)

if __name__ == "__main__":
    main()
