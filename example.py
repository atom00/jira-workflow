from jira import JIRA
from workflow import WorkflowManager
from selector import JiraSelector
from action import JiraAddCommentAction


def main():
    with open("conf_file", mode="r") as conf_file:
        conf = conf_file.read().splitlines()
    jira = JIRA(
        conf[0],
        basic_auth=(conf[1], conf[2]),
    )
    workflow_mgr = WorkflowManager(
        JiraSelector(jira, {"filter 1": "filter=10001"}),
        [JiraAddCommentAction(jira)],
    )
    workflow_mgr.run()


if __name__ == "__main__":
    main()
