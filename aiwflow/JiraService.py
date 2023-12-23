from jira import JIRA

from aiwflow.util import get_env_variable

JIRA_SERVICE_ADDRESS = get_env_variable('JIRA_SERVICE_ADDRESS')
EMAIL = get_env_variable('EMAIL')
JIRA_API_TOKEN = get_env_variable('JIRA_API_TOKEN')


class JiraService:
    def __init__(self):
        self.jira = JIRA(server=JIRA_SERVICE_ADDRESS,
                         basic_auth=(EMAIL, JIRA_API_TOKEN))

    def get_issue_summary(self, id: str):
        issue = self.jira.issue(id)
        return issue.fields.summary
