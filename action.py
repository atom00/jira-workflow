from abc import ABC, abstractmethod
from queue import LifoQueue
from jira import JIRA

from provider import JiraActionItem


class Action(ABC):
    @abstractmethod
    def run(self, item, stack: LifoQueue) -> None:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


class MainAction(Action):
    pass  # TODO


class SetupAction(Action):
    pass  # TODO


class BackAction(Action):
    def run(self, item, stack: LifoQueue) -> None:
        stack.get()
        stack.get().choose()

    def describe(self) -> str:
        return "Back"


class QuitAction(Action):
    def run(self, item, stack: LifoQueue) -> None:
        pass

    def describe(self) -> str:
        return "Quit"


class GitAction(Action):
    pass  # TODO


class JiraAction(Action):
    def __init__(self, jira_object: JIRA) -> None:
        self.jira = jira_object

    def run(self, item: JiraActionItem, stack: LifoQueue) -> None:
        raise NotImplementedError("Unimplemented jira action")

    def describe(self) -> str:
        return "Unimplemented generic jira action"


class JiraReadCommentsAction(JiraAction):
    def run(self, item: JiraActionItem, stack: LifoQueue) -> None:
        for comment in item.get_comments():
            print(comment)

        stack.get().choose()

    def describe(self) -> str:
        return "Display comments"


class JiraAddCommentAction(JiraAction):
    def run(self, item: JiraActionItem, stack: LifoQueue) -> None:
        item.add_comment("Test comment")  # TODO

        stack.get().choose()

    def describe(self) -> str:
        return "Add comment"
