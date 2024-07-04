from abc import ABC, abstractmethod
from queue import LifoQueue
from typing import List

from simple_term_menu import TerminalMenu

from action import Action
from provider import ActionItem, ActionItemProvider


class Choice(ABC):
    @abstractmethod
    def choose(self) -> None:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


class MenuChoice(Choice):
    def __init__(self, choices: List[str], stack: LifoQueue[Choice]) -> None:
        self.stack = stack
        self.menu = TerminalMenu(choices)

    @abstractmethod
    def _handle_selection(self, selected_id) -> None:
        pass

    def choose(self) -> None:
        self.stack.put(self)
        selected_id = self.menu.show()
        if selected_id is None:  # For example Ctrl+c case
            return

        self._handle_selection(selected_id)

    def describe(self) -> str:
        return "MenuChoice"


class ActionChoice(MenuChoice):
    def __init__(
        self,
        possible_actions: List[Action],
        action_item: ActionItem,
        stack: LifoQueue[Choice],
    ) -> None:
        self.possible_actions = possible_actions
        self.action_item = action_item
        super().__init__([action.describe() for action in possible_actions], stack)

    def _handle_selection(self, selected_id) -> None:
        self.possible_actions[selected_id].run(self.action_item, self.stack)

    def describe(self) -> str:
        return "ActionChoice"


class MainWorkflow(MenuChoice):
    def __init__(
        self,
        provider: ActionItemProvider,
        possible_actions: List[Action],
    ) -> None:
        self.action_items = provider.fetch()
        self.possible_actions = possible_actions
        super().__init__(
            [action_item.describe() for action_item in self.action_items], LifoQueue()
        )

    def _handle_selection(self, selected_id) -> None:
        action_choice = ActionChoice(
            self.possible_actions, self.action_items[selected_id], self.stack
        )
        action_choice.choose()

    def describe(self) -> str:
        return "ActionItemChoice"
