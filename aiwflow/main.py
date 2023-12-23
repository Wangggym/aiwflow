import typer
from aiwflow.Spinner import Spinner
from aiwflow.JiraService import JiraService
from aiwflow.llm import AI
from aiwflow.util import contains_only_english_with_special_chars, get_env_variable

main = typer.Typer()


@main.command()
def pr_create(ticket: str, issue_desc: str = None):
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


if __name__ == "__main__":
    main()
