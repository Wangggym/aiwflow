
from aiwflow.JiraService import JiraService
from aiwflow.Spinner import Spinner


def main():
    spinner = Spinner(JiraService().get_issue_summary, **{"id": "IRB-111"})
    print(spinner.result)

main()
