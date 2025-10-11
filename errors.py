from typing import Set


class ConfigException(Exception):
    def __init__(self, message):
        super().__init__(f"ConfigException: {message}")


class ConfigNotFound(ConfigException):
    def __init__(self, source):
        super().__init__(f"{source} was not found")


class ConfigWrongFormat(ConfigException):
    def __init__(self, source):
        super().__init__(f"{source} has wrong format (not csv)")


class ConfigUnexpectedField(ConfigException):
    def __init__(self, source, field):
        super().__init__(f"{source} has unexpected field: {field}")


class ConfigUnexpectedContent(ConfigException):
    def __init__(self, field, content, *allowed_content: Set[str]):
        super().__init__(f"Field {field} has unexpected content: {content}. Allowed content: {allowed_content}")


class ConfigUnexpectedFieldsAmount(ConfigException):
    def __init__(self, source, got, expected):
        super().__init__(f"{source} has unexpected number of fields: got {got}, expected {expected}")
