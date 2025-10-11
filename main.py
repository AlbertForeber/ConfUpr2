import csv
import os
from errors import *
from extras import ERROR, DEBUG, EXTRA

class DependencyTool:
    def __init__(self):

        self.__CONFIG_FILE_NAME = "config.csv"
        self.__params = {
            "name": "",
            "path": "",
            "data_mode": "",    # url or test
            "version": "",
            "show_ascii": "",  # true or false
            "filter": ""
        }

        self.__allowed_contents = {
            "data_mode": ("url", "test"),
            "show_ascii": ("true", "false")
        }

        try:
            self.__load_config()

            # TODO убрать после первого этапа
            print('-' * 40)
            print(DEBUG.format(f"Received arguments:"))
            for key in self.__params:
                print(f"+{DEBUG.format(key):>25}: {EXTRA.format(self.__params[key])}")
            print('-' * 40)
            #


        except ConfigException as e:
            print(ERROR.format(e))
            exit(1)


    def __load_config(self):
        if not os.path.exists(self.__CONFIG_FILE_NAME):
            raise ConfigNotFound(self.__CONFIG_FILE_NAME)

        if not self.__CONFIG_FILE_NAME.endswith(".csv"):
            raise ConfigWrongFormat(self.__CONFIG_FILE_NAME)

        csvfile = open(self.__CONFIG_FILE_NAME)
        reader = csv.reader(csvfile)

        fields_checked = []

        for field, content in reader:
            if field not in self.__params:
                raise ConfigUnexpectedField(self.__CONFIG_FILE_NAME, field)

            if not self.check_field_content(field, content):
                raise ConfigUnexpectedContent(field, content, *self.__allowed_contents[field])

            self.__params[field] = content
            fields_checked.append(field)

        len_fields_checked = len(set(fields_checked))
        expected_fields_checked = len(self.__params)

        if len_fields_checked != expected_fields_checked:
            raise ConfigUnexpectedFieldsAmount(self.__CONFIG_FILE_NAME, len_fields_checked, expected_fields_checked)


    def check_field_content(self, field, content):
        if field not in self.__allowed_contents:
            return True

        return False if content not in self.__allowed_contents[field] else True


if __name__ == "__main__":
    dep = DependencyTool()