from typing import List

import Task


class User:
    def __init__(self, task_list: List[Task], rate: int = 1):
        self.task_list = task_list
        self.rate = rate
