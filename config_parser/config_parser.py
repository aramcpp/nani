"""
Classes and functions for config parsing
"""

import os
import json

import jsonschema


class BaseConfigParserException(Exception):
    """Base exception for Config Parser"""
    pass


class ConfigFileNotFound(BaseConfigParserException):
    """Config file is not found exception"""
    pass


class Configs(object):
    """
    Config container
    """
    JSON_CONFIG_SCHEMA = {
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
                self.config_json = json.load(f)
        except json.JSONDecodeError:
            raise BaseConfigParserException("Failed to parse JSON")
        jsonschema.validate(
            instance=self.config_json,
            schema=self.__class__.JSON_CONFIG_SCHEMA
        )
