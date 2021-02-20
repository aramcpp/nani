from typing import Dict

from .task import Task
from .user import User


class Config:
    def __init__(
            self, host: str, port: int, scheme: str,
            task_dict: Dict[str, Task], user_dict: Dict[str, User]
    ):
        self.host = host
        self.port = port
        self.scheme = scheme
        self.task_dict = task_dict
        self.user_dict = user_dict
