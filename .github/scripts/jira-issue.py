## This script is used to create Jira bugs from CodeQL scan alerts.

# import os module
import os

# import requests module
import requests

# import json module
import json

token = os.environ['GITHUB_TOKEN']

jira_username = os.environ['JIRA_USERNAME']
jira_token = os.environ['JIRA_TOKEN']

jira_url = 'https://jsjiraapp.atlassian.net/rest/api/3/search'

jira_params = {
  'jql': 'project=STP',
  'issuetype': 'Bug'
}

jira_headers = {
    'Content-Type': 'application/json',
}

jira_auth = (jira_username, jira_token)

issue_details_response = requests.get(jira_url, params=jira_params, headers=jira_headers, auth=jira_auth)
issue_json = issue_details_response.json()
issue_list = issue_json['issues']
issue_codeql_list = []

## Checking for duplicate issues with custom field as CodeQL ID
# for issue in issue_list:
#   mapped_codeql_id = issue["fields"]["customfield_10043"]
#   issue_codeql_list.append(mapped_codeql_id)

## Checking for duplicate issues with title
for issue in issue_list:
  jira_issue_title = issue["fields"]["summary"]
  issue_codeql_list.append(jira_issue_title)

# store API url
url = 'https://api.github.com/repos/jayseth/sample-actions/code-scanning/alerts'

# assign the headers- not always necessary, but something we have to do with the GitHub API
headers = {'Accept': 'application/vnd.github+json',
          'Authorization': "Bearer {}".format(token),
          'X-GitHub-Api-Version': '2022-11-28'}

# assign the requests method
r = requests.get(url, headers=headers)

def get_json(r):
  if r.status_code == 200:             
    # store API response to variable
    alert_list = r.json()
    
    json_obj = {}
    json_obj['details'] = []
    summary_prefix = 'CodeQL ('
    summary_filler = ') '
    summary_line = ' Line '
    summary_colon = ': '
    summary_hyphen = ' - '
    desc_prefix = 'CodeQL scan alert "'
    desc_filler = '" found in '

    ## iterating through the list of objects of CodeQL scan alerts
    for alert in alert_list:
      alert_dict = {}
      if alert['state'] == 'open':

        url = alert['html_url']
        severity = alert['rule']['severity']
        rule_desc = alert['rule']['description']
        location = alert['most_recent_instance']['location']['path']
        line_no = alert['most_recent_instance']['location']['start_line']
        alert_name = alert['most_recent_instance']['message']['text']
        
        alert_dict['name'] = summary_prefix + severity + summary_filler + location + summary_line + str(line_no) + summary_colon + rule_desc + summary_hyphen + alert_name 
        alert_dict['description'] = desc_prefix + alert_name + desc_filler + url
       
        if alert_dict['name'] in issue_codeql_list:
          continue
        else:
          json_obj['details'].append(alert_dict)
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
