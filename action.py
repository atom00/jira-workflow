from abc import ABC, abstractmethod
from jira import JIRA

from selector import JiraActionItem


class Action(ABC):
    @abstractmethod
    def run(self, item) -> None:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


class MainAction(Action):
    pass  # TODO


class SetupAction(Action):
    pass  # TODO


class GitAction(Action):
    pass  # TODO


class JiraAction(Action):
    def __init__(self, jira_object: JIRA) -> None:
        self.jira = jira_object

    def run(self, item: JiraActionItem) -> None:
        raise NotImplementedError("Unimplemented jira action")

    def describe(self) -> str:
        return "Unimplemented generic jira action"


class JiraAddCommentAction(JiraAction):
    def run(self, item: JiraActionItem) -> None:
        item.add_comment("Test comment")  # TODO

    def describe(self) -> str:
        return "Add comment"
