## Contents of .github/scripts folder

### `codeql-create-jira-issue.py` is a python script that does the following:
- gets details of CodeQL scan alerts from GitHub
- gets details of existing Jira bugs from Jira which is then used to test for duplicates
- compiles and creates a json consisting of details required to create Jira bugs which is then passed as a job output to the workflow that calls this script

### `sonar-create-jira-issue.py` is a pyhton script that does the following:
- Import Dependencies:
       The script begins by importing necessary modules, including os for environment variables, requests for making         HTTP requests, and json for handling JSON data.
- Define SonarQube API and Token:
       The script defines the SonarQube API endpoint (sonar_url) and retrieves the SonarQube authentication token            from an environment variable (SONAR_TOKEN).
- Set Up Headers for the Request:
       The script sets up HTTP headers, including the authorization header with the SonarQube token, for making a            request to the SonarQube API.
- Make a Request to SonarQube:
       The script uses the requests.get method to send an HTTP GET request to the SonarQube API, including the               authentication headers.
- Check Response Status:
       The script checks if the response status code is 200 (indicating a successful request).
- Extract and Process SonarQube Data:
       If the response is successful, the script extracts and processes the JSON data from the response. It retrieves        the project's status and conditions.
- Identify Error Metrics:
       The script iterates through the conditions and identifies metrics with 'ERROR' status, removing the 'new_'            prefix if present. These metrics are added to the error_metrics set.
- Quality Gate Status Check:
       The script checks the overall project status. If it's not 'OK,' indicating issues with the quality gate, the          script proceeds to create a JIRA issue.
- Create a JIRA Issue:
        If the quality gate status is not 'OK,' the script creates a JIRA issue. It retrieves the JIRA username and           token from environment variables, sets up headers and authentication for the JIRA request, and constructs a           JIRA issue payload with a summary and description that includes information about the error metrics.
- Check JIRA Issue Creation:
        The script checks if the JIRA issue creation was successful (status code 201). If successful, it prints a             message indicating that a new issue was created in JIRA. If not, it prints an error message.
- Exit Code Handling:
        The script uses exit(1) to exit with a non-zero status code if the quality gate is not passed. This non-zero          exit code can be used in CI/CD pipelines to indicate a failure.
- Final Output:
        The script prints messages indicating whether the SonarQube analysis passed without issues or if there were           vulnerabilities detected.

