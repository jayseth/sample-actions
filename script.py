import os
import requests
import json

# SonarQube API endpoint
sonar_url = 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Github-Test-Org'

# SonarQube authentication token
sonar_token = os.environ['SONAR_TOKEN']

# Set up headers for the request
headers = {
    'Authorization': sonar_token,
}

# Make the request to SonarQube
response = requests.get(sonar_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    report = response.json()
    
    # Extract relevant information from the response
    status = report['projectStatus']['status']
    conditions = report['projectStatus']['conditions']
    
    # Filter conditions with status other than 'OK'
    failed_conditions = [f"{condition['metricKey']}: {condition['actualValue']} / {condition['errorThreshold']} ({condition['status']})"
                         for condition in conditions if condition['status'] != 'OK']
    
    result = ', '.join(failed_conditions)
    
    if status != 'OK':
        print("SonarQube analysis failed! Vulnerabilities found.")
        
        # Creating JIRA Issue
        jira_url = 'https://jsjiraapp.atlassian.net/rest/api/2/issue'
        jira_username = os.environ['JIRA_USERNAME']
        jira_token = os.environ['JIRA_TOKEN']
        
        # Set up headers for the JIRA request
        jira_headers = {
            'Content-Type': 'application/json',
        }
        
        # Set up authentication for the JIRA request
        jira_auth = (jira_username, jira_token)
        
        # Create JIRA issue payload
        jira_payload = {
            "fields": {
                "project": {"key": "SON"},
                "summary": f"SonarQube analysis failed with error code {status}!",
                "description": result,
                "issuetype": {"name": "Task"}
            }
        }
        
        # Make the request to create a JIRA issue
        jira_response = requests.post(jira_url, json=jira_payload, headers=jira_headers, auth=jira_auth)
        
        # Check if the JIRA issue was created successfully
        if jira_response.status_code == 201:
            print("Created a new issue in Jira.")
        else:
            print(f"Failed to create JIRA issue. Status code: {jira_response.status_code}")
        
        exit(1)
    else:
        print("SonarQube analysis passed. No vulnerabilities found.")

else:
    print(f"Failed to retrieve SonarQube project status. Status code: {response.status_code}")
