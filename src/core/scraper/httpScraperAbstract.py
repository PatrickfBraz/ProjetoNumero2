"""
O objetivo deste modulo é servir de abstrato no tratamento e na chamada das classes filhas de busca de dados.
Desta forma, o usuário pode implementar diversos outros scrapers com logicas e fontes diferentes.
"""
import importlib
import logging
from os import getenv
import functools
import time
from src.core.storage.storageInterface import get_storage_engine
from src.logger.loggerConfig import CustomLogger


def http_scraper_execution_timer(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = CustomLogger().get_logger()
        start_time = time.perf_counter()
        value = function(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f" httpScraper info: método {function.__name__!r} executou em {run_time:.4f} seg")
        return value

    return wrapper


def initialize_scraper_engine(logger: logging = None):
    module_name = getenv("SCRAPER_ENGINE")
    module_path = ".".join(["src", "core", "scraper", "engines", module_name])
    try:
        if logger:
            logger.debug(f"Inicializando modulo: {module_name}")
            logger.debug(f"Caminho ate o modulo: {module_path}")

        engine = importlib.import_module(module_path)
        scraper = engine.HttpScraper(logger)
        scraper.execute()
    except TypeError as type_error:
        if logger:
            logger.critical(f"Erro na importacao do modulo {module_name}: {type_error}")
        pass
    except ModuleNotFoundError:
        if logger:
            logger.critical(f"Modulo {module_name} não encontrado no caminho {module_path}")
        pass


class HttpScraperAbstract:
    def __init__(self, logger=None):
        self.module_name = getenv("SCRAPER_ENGINE")
        self.logger = logger if logger else CustomLogger().get_logger()
        self.max_retries = int(getenv("SCRAPER_MAX_RETRIES"))
        self.timeout = int(getenv("SCRAPER_REQUEST_TIMEOUT"))
        self.storage_interface = get_storage_engine(self.logger)
        self.current_request: object = None

    def make_request(self, request_method, url: str, custom_header: dict = None):
        try:
            # todo Ampliar metodo para suportar autenticação na requisição
            retry = 0
            while retry <= self.max_retries:
                self.logger.debug(f"Método: {request_method.__name__}| Tentativa: {retry}")
                try:
                    if custom_header:
                        self.current_request = request_method(url=url, headers=custom_header, timeout=self.timeout)
                        break
                    else:
                        self.current_request = request_method(url=url, timeout=self.timeout)
                        break
                except TimeoutError:
                    self.current_request = None
                    retry += 1

            if retry == self.max_retries and self.current_request is None:
                self.logger.error(f"Erro de timeout ao acessar: {url}")
                self.current_request = None
            elif retry < self.max_retries and self.current_request is None:
                self.logger.error(f"Erro inesperado ao tentar acessar: {url}")
        except ValueError as error:
            self.logger.critical(f"{error}")
            self.current_request = None
