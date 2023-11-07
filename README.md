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
     
