## This script is used to create Jira bugs from GitHub issues

# import os module
import os

# import requests module
import requests

# import json module
import json

##### JIRA DETAILS #####

jira_username = os.environ['JIRA_USER_EMAIL']
jira_token = os.environ['JIRA_API_TOKEN']

jira_url = 'https://jsjiraapp.atlassian.net/rest/api/3/search'

jira_params = {
  'jql': 'project=STP',
  'issuetype': 'Bug'
}

# Set up headers for the JIRA request
jira_headers = {
    'Content-Type': 'application/json',
}

# Set up authentication for the JIRA request
jira_auth = (jira_username, jira_token)

issue_details_response = requests.get(jira_url, params=jira_params, headers=jira_headers, auth=jira_auth)
issue_json = issue_details_response.json()
jira_issue_list = issue_json['issues']
issue_github_list = []

for jira_issue in jira_issue_list:
  mapped_github_issue_id = jira_issue["fields"]["customfield_10044"]
  issue_github_list.append(mapped_github_issue_id)

##### GITHUB ISSUE DETAILS #####

# store API url
url = 'https://api.github.com/repos/anauskadutta/sample1/issues'

# assign the headers- not always necessary, but something we have to do with the GitHub API
headers = {'Accept': 'application/vnd.github.v3+json'}

# assign the requests method
r = requests.get(url, headers=headers)

def get_json(r):
  if r.status_code == 200:
    gh_issue_list = r.json()
    json_obj = {}
    json_obj['details'] = []

    ## iterating through the list of objects of GitHub issues
    for gh_issue in gh_issue_list:
      issue_obj = {}
      if gh_issue['state'] == 'open':
        issue_obj['id'] = gh_issue['number']
        issue_obj['name'] = gh_issue['title']
        issue_obj['url'] = gh_issue['html_url']
        if issue_obj['id'] in issue_github_list:
          continue
        else:
          json_obj['details'].append(issue_obj)
      else:
        continue

    if json_obj['details'] == []:
      json_obj = {}
    
    json_data = json.dumps(json_obj)
    
  else:
    print(f"Status code: {r.status_code}")
    print(r.json())

  return json_data

print(get_json(r))
