### `Dotnet_Build_Sonar_Scan.yml` is a GitHub workflow that does the following:
- Builds the Dotnet App and Scans it using SonarQube Scan uploading the results to SonarQube Quality Gate

### `Sonar_Python_Jira.yml` is a GitHub workflow that does the following:
- Retrieves SonarQube Quality Gate status and creates JIRA Issues if any vulnerabilities are detected

### `codeql.yml` is a GitHub workflow that does the following:
- performs CodeQL analysis on the codebase and uploads the results to GitHub under the Security tab
 
### `get-codeql-vulnerability-details.yml` is a GitHub workflow that does the following:
- calls and executes the `codeql-create-jira-issue.yml` script and passes the json output to the next workflow
 
### `codeql-create-jira-issue.yml` is a GitHub workflow that does the following:
- creates Jira bugs using the json output from the `get-codeql-vulnerability-details.yml` workflow

### `Sonar_CodeQL_JIRA.yml` is a GitHub workflow that does the following:
- Combines all the above workflows and runs them as a single integrated workflow
