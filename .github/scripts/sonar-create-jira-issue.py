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
    print(report)
    
    # Extract relevant information from the response
    status = report['projectStatus']['status']
    conditions = report['projectStatus']['conditions']

    error_metrics = set()

    for condition in report['projectStatus']['conditions']:
        metric_key = condition['metricKey']
        # Check if the metric has 'ERROR' status
        if condition['status'] == 'ERROR':
            # Remove 'new_' prefix if present
            metric_key = metric_key.replace('new_', '', 1)
            error_metrics.add(metric_key)
    
    if status != 'OK':
        print("SonarQube analysis failed! Vulnerabilities found.")

        error_message = "Your application did not pass the Quality gate since it has problems with these key metrics:"

        # Creating JIRA Issue
        jira_url = os.environ['JIRA_URL']
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
                "summary": f"SonarQube analysis failed!",
                "description": f"{error_message}\n" + "\n".join([f"{index}. {metric}" for index, metric in enumerate(error_metrics, start=1)]),
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
        
        # exit(1)
    else:
        print("SonarQube analysis passed. No vulnerabilities found.")

else:
    print(f"Failed to retrieve SonarQube project status. Status code: {response.status_code}")
