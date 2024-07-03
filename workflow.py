from action import Action
from typing import List
from selector import Selector
from simple_term_menu import TerminalMenu


class WorkflowManager:
    def __init__(self, selector: Selector, actions: List[Action]) -> None:
        self.actions = actions
        self.action_items = selector.get_items()
        self.main_menu = TerminalMenu(
            [item.describe() for item in list(self.action_items.values())[0]]
        )  # TODO
        self.action_menu = TerminalMenu([item.describe() for item in actions])

    def run(self):
        selected_item = self.main_menu.show()
        selected_action = self.action_menu.show()
        self.actions[selected_action].run(
            list(self.action_items.values())[0][selected_item]
        )
