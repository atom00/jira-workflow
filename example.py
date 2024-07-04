from jira import JIRA
from action import BackAction, JiraAddCommentAction, JiraReadCommentsAction, QuitAction
from choice import MainWorkflow
from provider import JiraProvider


def main():
    with open("/home/tbohutyn/tmp/conf_file", mode="r") as conf_file:
        conf = conf_file.read().splitlines()
    jira = JIRA(
        conf[0],
        basic_auth=(conf[1], conf[2]),
    )
    workflow_mgr = MainWorkflow(
        JiraProvider(
            jira,
            "filter=10001",
        ),
        [
            JiraReadCommentsAction(jira),
            JiraAddCommentAction(jira),
            BackAction(),
            QuitAction(),
        ],
    )
    workflow_mgr.choose()


if __name__ == "__main__":
    main()
