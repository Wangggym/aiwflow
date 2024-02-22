import typer
import json
from aiwflow.Spinner import Spinner
from aiwflow.JiraService import JiraService
from aiwflow.llm import AI
from aiwflow.util import contains_only_english_with_special_chars, get_env_variable, is_long_desc

main = typer.Typer()


class Issue:
    issue_desc: str = None
    translated_desc: str = None
    need_translate: bool = False
    error: Exception = None

    def __init__(self):
        issue_desc: str = None
        translated_desc: str = None
        need_translate: bool = False
        error: Exception = None


@main.command()
def pr_create(ticket: str, issue_desc: str = None):
    if issue_desc is not None:
        print(f"{issue_desc}")
        return

    issue_desc = JiraService().get_issue_summary(id=ticket)

    if contains_only_english_with_special_chars(issue_desc) is True:
        print(f"{issue_desc}")
        return

    translated_desc = AI().translate(desc=issue_desc)
    print(f"{translated_desc}")
    return


def summarize(issue: Issue):
    if contains_only_english_with_special_chars(issue.issue_desc) is True and is_long_desc(issue.issue_desc) is False:
        issue.need_translate = False
        print(json.dumps(issue.__dict__, ensure_ascii=False))
        return

    try:
        issue.need_translate = True
        issue.translated_desc = AI().translate(desc=issue.issue_desc)
        print(json.dumps(issue.__dict__, ensure_ascii=False))
    except Exception as error:
        print(json.dumps(issue.__dict__, ensure_ascii=False))
        return


@main.command()
def issue_desc(ticket: str):
    issue = Issue()
    try:
        issue.issue_desc = JiraService().get_issue_summary(id=ticket)
    except Exception as error:
        print(json.dumps(issue.__dict__, ensure_ascii=False))
        return

    summarize(issue)


@main.command()
def summary(desc: str):
    issue = Issue()
    issue.issue_desc = desc
    summarize(issue)


@main.command()
def pr_create_v2(ticket: str, issue_desc: str = None):
    if issue_desc is not None:
        print(f"{issue_desc}")
        return

    spinner = Spinner(JiraService().get_issue_summary, **{"id": ticket})
    issue_desc = spinner.result

    if contains_only_english_with_special_chars(issue_desc) is True:
        print(f"{issue_desc}")
        return

    print(f"\033[32m\u2713\033[0m Get jira ticket description: {issue_desc}")
    print('AI translating...')

    spinnerAI = Spinner(AI().translate, **{"desc": issue_desc})
    print(f"{spinnerAI.result}")
    return


@main.command()
def me():
    email = get_env_variable('EMAIL')
    print(email)


@main.command()
def jira_add_comment(ticket: str, comment: str):
    JiraService().jira.add_comment(ticket, comment)


if __name__ == "__main__":
    main()
