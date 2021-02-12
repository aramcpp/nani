from typing import List

import Task


class Config:
    def __init__(self, host: str, port: int, scheme: str, task_list: List[Task], user_list: List[User]):
        self.host = host
        self.port = port
        self.scheme = scheme
        self.task_list = task_list
        self.user_list = user_list
