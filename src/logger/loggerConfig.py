"""
Este módulo contem a classe de configuração de logger. Ela irá carregar as configurações de logger definidas pelo
usuario em tempo de execução para gerar o basicConfig do logger.
"""
import logging
from os import getenv
from os.path import join, exists
from datetime import datetime
from src.error.error_types import LoggerGenerationError


class CustomLogger:
    """
    Esta é uma classe básica de geração de logger.
    """

    def __init__(self):
        level = getenv("LOGGER_LEVEL")
        self.logger = logging.getLogger()
        self.logFormat = getenv("LOGGER_FORMAT")

        if level == 'DEBUG':
            self.level = logging.DEBUG
        elif level == 'INFO':
            self.level = logging.INFO
        elif level == 'WARNING':
            self.level = logging.WARNING
        elif level == 'ERROR':
            self.level = logging.ERROR
        elif level == 'CRITICAL':
            self.level = logging.CRITICAL

    def get_logger(self):
        """
        Método responsável por retornar um objeto logger configurado.
        """
        try:
            self.logger = logging.getLogger()
            if self.logger.handlers:
                for handler in self.logger.handlers:
                    self.logger.removeHandler(handler)
            if getenv("LOGGER_STORAGE_PATH"):
                if exists(join(getenv("LOGGER_STORAGE_PATH"),
                               ("logger_" + datetime.now().strftime("%d-%m-%Y-%H:%M:%S")))):
                    print("Ta aqui")
                    logging.basicConfig(
                        filename=join(getenv("LOGGER_STORAGE_PATH"),
                                      ("logger_" + datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))),
                        format=self.logFormat,
                        filemode='a',
                        datefmt="%d/%m/%Y %H:%M:%S",
                        level=self.level
                    )
                else:
                    logging.basicConfig(
                        filename=join(getenv("LOGGER_STORAGE_PATH"),
                                      ("logger_" + datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))),
                        format=self.logFormat,
                        filemode='w',
                        datefmt="%d/%m/%Y %H:%M:%S",
                        level=self.level
                    )
            else:
                logging.basicConfig(
                    format=self.logFormat,
                    datefmt="%d/%m/%Y %H:%M:%S",
                    level=self.level
                )
            return self.logger
        except FileNotFoundError as error:
            raise LoggerGenerationError(f"{error}")
