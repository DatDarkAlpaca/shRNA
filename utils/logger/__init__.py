import logging.config
import coloredlogs
import logging
import yaml


class Logger:
    initialized = False

    def __init__(self, logger_name: str, level: str = 'INFO'):
        self.logger = logging.getLogger(logger_name)

        if not Logger.initialized:
            Logger._initialize()

        coloredlogs.install(level=level, logger=self.logger)
        coloredlogs.install(level=None)

    @staticmethod
    def _initialize():
        config_filepath = './res/log/config.yaml'
        with open(config_filepath, mode='r', encoding='utf-8') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)
