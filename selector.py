from abc import ABC, abstractmethod
from typing import List, Dict
from jira import JIRA
from jira.resources import Issue


class ActionItem(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass


class Selector(ABC):
    @abstractmethod
    def get_items(self) -> Dict[str, List[ActionItem]]:
        pass


class JiraActionItem(ActionItem):
    def __init__(self, jira_object: JIRA, issue: Issue) -> None:
        super().__init__()
        self.jira = jira_object
        self.issue = issue

    def describe(self) -> str:
        return self.issue.key

    def add_comment(self, content: str) -> None:
        self.jira.add_comment(self.issue, content)


class JiraSelector(Selector):
    def __init__(self, jira_object: JIRA, filter_dict: Dict[str, str]) -> None:
        super().__init__()
        self.jira = jira_object
        self.filter_dict = filter_dict

    def get_items(self) -> Dict[str, List[JiraActionItem]]:
        return {
            desc: list(
                map(
                    lambda issue: JiraActionItem(self.jira, issue),
                    self.jira.search_issues(jira_filter),
                )
            )
            for desc, jira_filter in self.filter_dict.items()
        }
