import logging
import configparser
from common.utility import GlobalVariable


class ConfigManager(object):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(GlobalVariable.config_file_name)

    def get_value(self, section, key):
        try:
            value = self.config.get(section, key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_author_value(self, key):
        try:
            value = self.config.get("AUTHOR", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_app_value(self, key):
        try:
            value = self.config.get("APP", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_sms_value(self, key):
        try:
            value = self.config.get("SMS", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_cache_value(self, key):
        try:
            value = self.config.get("CACHE", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_database_value(self, key):
        try:
            value = self.config.get("DATABASE", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_path_value(self, key):
        try:
            value = self.config.get("PATH", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_optimization_value(self, key):
        try:
            value = self.config.get("OPTIMIZATION", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_picture_value(self, key):
        try:
            value = self.config.get("PICTURE", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

    def get_model_value(self, key):
        try:
            value = self.config.get("MODEL", key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value
