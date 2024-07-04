from abc import ABC, abstractmethod
from typing import List, Sequence
from jira import JIRA
from jira.resources import Issue
from datetime import datetime


class ActionItem(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass


class ActionItemProvider(ABC):
    @abstractmethod
    def fetch(self) -> Sequence[ActionItem]:
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

    @staticmethod
    def _format_jira_date(datestr: str) -> str:
        iso_format_datestr = datestr[:-2] + ":" + datestr[-2:]
        return datetime.fromisoformat(iso_format_datestr).strftime("%Y-%m-%d %H:%M:%S")

    def get_comments(self) -> List[str]:
        return list(
            map(
                lambda comment: f"{comment.author.displayName}   [{self._format_jira_date(comment.created)}]\n{comment.body}",
                self.jira.comments(self.issue.key),
            )
        )


class JiraProvider(ActionItemProvider):
    def __init__(
        self,
        jira_object: JIRA,
        jira_filter: str,
    ) -> None:
        super().__init__()
        self.jira = jira_object
        self.jira_filter = jira_filter

    def fetch(self) -> List[JiraActionItem]:
        return list(
            map(
                lambda issue: JiraActionItem(self.jira, issue),
                self.jira.search_issues(self.jira_filter),
            )
        )
