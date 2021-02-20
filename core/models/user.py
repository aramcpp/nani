from typing import List

from .task import Task


class User:
    def __init__(self, name: str, task_list: List[Task], rate: int = 1):
        self.name = name
        self.task_list = task_list
        self.rate = rate
