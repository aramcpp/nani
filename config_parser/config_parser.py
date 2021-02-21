"""
Classes and functions for config parsing
"""

import os
import json
from typing import Dict

import jsonschema

from core.models.config import Config
from core.models.task import Task
from core.models.user import User


class BaseConfigParserException(Exception):
    """Base exception for Config Parser"""
    pass


class ConfigFileNotFound(BaseConfigParserException):
    """Config file is not found exception"""
    pass


class ConfigParser(object):
    """
    Config container
    """
    __JSON_CONFIG_SCHEMA = {
        "type": "object",
        "properties": {
            "host": {"type": "string"},
            "port": {
                "type": "integer",
                "minimum": 0,
                "maximum": 65535,
            },
            "scheme": {
                "type": "string",
                "enum": ["http", "https"],
            },
            "tasks": {
                "type": "object",
                "patternProperties": {
                    ".*": {
                        "type": "object",
                        "properties": {
                            "method": {
                                "type": "string",
                                "enum": ["GET", "POST"],
                            },
                            "endpoint": {
                                "type": "string",
                                "minLength": 1,
                            },
                            "payload": {
                                "type": "object",
                            },
                            "headers": {
                                "type": "object",
                            }
                        },
                        "required": ["method", "endpoint"]
                    },
                },
            },
            "users": {
                "type": "object",
                "patternProperties": {
                    ".*": {
                        "type": "object",
                        "properties": {
                            "tasks": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "minItems": 2,
                            },
                            "rate": {
                                "type": "number",
                                "minimum": 0,
                            }
                        },
                        "required": ["tasks"],
                    },
                }
            },
        },
        "required": ["host", "port", "scheme", "tasks", "users"],
    }

    def __init__(self, config_file):
        if not os.path.isfile(config_file):
            raise ConfigFileNotFound(
                "%s is not a file or does not exist" % config_file
            )

        try:
            with open(config_file, 'r') as f:
                self._config_json = json.load(f)
        except json.JSONDecodeError:
            raise BaseConfigParserException("Failed to parse JSON")
        try:
            jsonschema.validate(
                instance=self._config_json,
                schema=self.__class__.__JSON_CONFIG_SCHEMA
            )
        except jsonschema.exceptions.ValidationError as e:
            raise BaseConfigParserException(e.message)

        users_dict = self._config_json.get("users")
        tasks_dict = self._config_json.get("tasks")
        host = self._config_json.get("host")
        port = self._config_json.get("port")
        scheme = self._config_json.get("scheme")
        self._tasks = self.process_tasks_dict(tasks_dict)
        self._users = self.process_users_dict(users_dict)
        self._config = Config(
            host=host,
            port=port,
            scheme=scheme,
            task_dict=self._tasks,
            user_dict=self._users,
        )

    @staticmethod
    def process_tasks_dict(tasks_dict) -> Dict[str, Task]:
        tasks = {}
        for task_name, task_properties in tasks_dict.items():
            current_task = Task(
                name=task_name,
                method=task_properties.get("method"),
                endpoint=task_properties.get("endpoint"),
                headers=task_properties.get("headers"),
                payload=task_properties.get("payload"),
            )
            tasks[task_name] = current_task
        return tasks

    def process_users_dict(self, users_dict: Dict) -> Dict[str, User]:
        users = {}
        for user_name, user_properties in users_dict.items():
            user_task_names = user_properties.get("tasks")
            user_tasks = []
            for task_name in user_task_names:
                current_task = self.get_task(task_name)
                if current_task is None:
                    raise BaseConfigParserException("Task %s does not exist for user %s" % (task_name, user_name))
                else:
                    user_tasks.append(current_task)
            user_rate = user_properties.get("rate", 1)
            current_user = User(
                name=user_name,
                task_list=user_tasks,
                rate=user_rate,
            )
            users[user_name] = current_user
        return users

    def get_task(self, task_name: str) -> Task:
        return self._tasks.get(task_name)

    def get_config(self) -> Config:
        return self._config
