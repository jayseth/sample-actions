# SonarQube & JIRA for .NET using GitHub Actions

## Objective
To run a SonarQube Scan on a .NET application using GitHub actions and create a JIRA Issue for any vulnerabilities found in the scan. 

## Introduction
This repository has two segments:
  1. The DotNet Application
  2. GitHub Workflows

The following diagram shows how the actions and the application are integrated to achieve the use case:
![GitHub Actions](https://github.com/jayseth/sample-actions/assets/46541147/37734274-ebca-4626-ac5d-ecd4cc9cbbba)

## .NET Application
The application is a straightword DotNet App with a few vulnerabilities purposely injected to Flag in SonarQube
  1. The application defines a class named Program with several methods.
  2. The apiKey variable is hard-coded with an API key, which should not be done in a production application. Storing   sensitive information in source code is a security risk.
  3. The Main method is the entry point and calls ExecuteQuery and CallApi methods.
  4. The ExecuteQuery method constructs a SQL query without using parameterized queries. This is a vulnerability that   can lead to SQL injection.
  5. The DisplayMessage method creates an HTML string from a message, but it's not used in the Main method.
  6. The CallApi method prints a message indicating that an API call is made.
  7. The Example method creates a temporary file and writes content to it. This is a Security Vulnerability.

## Sonar Scan Workflow
  1. Workflow Configuration:
      The workflow is triggered on both workflow_call and manual workflow_dispatch events, allowing you to run it           manually or as part of other workflows.
  2. Job Configuration (JIRA_Process):
       This job runs on an Ubuntu latest runner.
  3. Checkout Repository:
       Uses the actions/checkout action to check out the source code from the repository. It disables shallow clone          by setting fetch-depth to 0.
  4. Setup .NET Core SDK:
       Uses the actions/setup-dotnet action to set up the .NET Core SDK.
  5. Install Dependencies:
       Runs dotnet restore to install project dependencies.
  6. SonarQube Analysis Begin:
       Installs the dotnet-sonarscanner tool globally.
       Executes dotnet sonarscanner begin to start the SonarQube analysis. It specifies the organizatioN                     (/o:jayseth), project key (/k:Github-Test-Org), and sets various parameters, including the SonarQube login            token from GitHub secrets and the path to the SonarQube analysis XML file.
  7. Build:
       Runs dotnet build to build the .NET project.
  8. Test with the dotnet CLI:
       Runs unit tests using dotnet test and specifies the test settings using a runsettings file. It also specifies         the environment variable ASPNETCORE_ENVIRONMENT as "Development."
  9. SonarQube Analysis End:
        Executes dotnet sonarscanner end to complete the SonarQube analysis. It uses the SonarQube login token from           GitHub secrets and sets the GITHUB_TOKEN environment variable.

## JIRA Github Workflow
  1. Workflow Configuration:
       The workflow is triggered on both workflow_call and manual workflow_dispatch events, allowing you to run it           manually or as part of other workflows.
  2. Job Configuration (JIRA_Process):
       This job runs on an Ubuntu latest runner.
  3. Checkout Repository:
       The actions/checkout action is used to fetch the source code from the repository. The fetch-depth: 0 option is        set to perform a full clone.
  4. Set up Python:
       The actions/setup-python action is used to set up Python with a specified version (3.x).
  5. Install Dependencies:
       The workflow installs or upgrades pip and installs the requests library to enable making HTTP requests in the         Python script.
  6. Make Python Requests:
       The run step executes the script.py script using the Python interpreter. It also defines environment variables        for the script to use, including SONAR_TOKEN, JIRA_USERNAME, and JIRA_TOKEN, which are retrieved from GitHub          secrets.

## Sonar JIRA Integration using Pyhton
  1. Import Dependencies:
       The script begins by importing necessary modules, including os for environment variables, requests for making         HTTP requests, and json for handling JSON data.
  2. Define SonarQube API and Token:
       The script defines the SonarQube API endpoint (sonar_url) and retrieves the SonarQube authentication token            from an environment variable (SONAR_TOKEN).
  3. Set Up Headers for the Request:
       The script sets up HTTP headers, including the authorization header with the SonarQube token, for making a            request to the SonarQube API.
  4. Make a Request to SonarQube:
       The script uses the requests.get method to send an HTTP GET request to the SonarQube API, including the               authentication headers.
  5. Check Response Status:
       The script checks if the response status code is 200 (indicating a successful request).
  6. Extract and Process SonarQube Data:
       If the response is successful, the script extracts and processes the JSON data from the response. It retrieves        the project's status and conditions.
  7. Identify Error Metrics:
       The script iterates through the conditions and identifies metrics with 'ERROR' status, removing the 'new_'            prefix if present. These metrics are added to the error_metrics set.
  8. Quality Gate Status Check:
       The script checks the overall project status. If it's not 'OK,' indicating issues with the quality gate, the          script proceeds to create a JIRA issue.
  9. Create a JIRA Issue:
        If the quality gate status is not 'OK,' the script creates a JIRA issue. It retrieves the JIRA username and           token from environment variables, sets up headers and authentication for the JIRA request, and constructs a           JIRA issue payload with a summary and description that includes information about the error metrics.
  10. Check JIRA Issue Creation:
        The script checks if the JIRA issue creation was successful (status code 201). If successful, it prints a             message indicating that a new issue was created in JIRA. If not, it prints an error message.
  11. Exit Code Handling:
        The script uses exit(1) to exit with a non-zero status code if the quality gate is not passed. This non-zero          exit code can be used in CI/CD pipelines to indicate a failure.
  12. Final Output:
        The script prints messages indicating whether the SonarQube analysis passed without issues or if there were           vulnerabilities detected.

## Combining the Workflows
  1. Workflow Configuration:
       The workflow is named "Combined Workflow" and is triggered manually using workflow_dispatch.
  2. SonarScan Job:
       This job is defined using the SonarScan key.
       It uses a workflow template defined in the file ./.github/workflows/BuildScan.yml with the uses keyword.
  3. The secrets:
     Inherit statement suggests that this job should inherit the secrets defined in the parent workflow. Secrets are       securely passed between jobs using this method.
  4. JIRA_Process Job:
       This job is defined using the JIRA_Process key.
       It is dependent on the successful completion of the SonarScan job. The needs keyword ensures that JIRA_Process        won't run until SonarScan has completed successfully.
       It uses a workflow template defined in the file ./.github/workflows/Python_JIRA.yml with the uses keyword.
       Similar to the SonarScan job, it also inherits secrets from the parent workflow.
     
