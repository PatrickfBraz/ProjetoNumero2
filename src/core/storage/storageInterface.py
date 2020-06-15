"""
modulo não implementado
"""
from src.logger.loggerConfig import CustomLogger
from os import getenv
import logging
import importlib


def get_storage_engine(logger: logging = None):
    """
    Esta função tem o objetivo de retornar um objeto do modulo que será utilizado para salvar e tratar os dados buscados
    pelo scraper.
    """
    module_name = getenv("STORAGE_ENGINE")
    module_path = ".".join(["src", "core", "storage", "engines", module_name])
    try:
        if logger:
            logger.debug(f"Inicializando modulo: {module_name}")
            logger.debug(f"Caminho ate o modulo: {module_path}")

        engine = importlib.import_module(module_path)
        storage = engine.Storage(logger)
        return storage
    except TypeError as type_error:
        if logger:
            logger.critical(f"Erro na importacao do modulo {module_name}: {type_error}")
        # todo definir que tipo de excecao sera disparado
        pass
    except ModuleNotFoundError:
        if logger:
            logger.critical(f"Modulo {module_name} não encontrado no caminho {module_path}")
        # todo definir que tipo de excecao sera disparado
        pass


class StorageInterface:
    def __init__(self, logger=None):
        self.logger = logger if logger else CustomLogger().get_logger()
        self.module_name = getenv("STORAGE_ENGINE")
        self.data_encoding = getenv("STORAGE_DATA_ENCODING")
        self.local_path = getenv("STORAGE_LOCAL_PATH")
