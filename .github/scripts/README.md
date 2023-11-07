## Contents of this folder

### `jira-issue.py` is a python script that does the following:
- gets details of CodeQL scan alerts from GitHub
- gets details of existing Jira bugs from Jira which is then used to test for duplicates
- compiles and creates a json consisting of details required to create Jira bugs which is then passed as a job output to the workflow that calls this script
