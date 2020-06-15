"""
Este modulo possui a classe responsável pela leitura em tempo de execução das configurações passadas pelo usuário.
"""
import os
import json
from src.error.error_types import ExecutionConfigurationLoadError


class ConfigLoader:
    """
    Esta classe é responsável por ler o arquivo de parametros de execução e criar as variaveis de ambiente as quais
    serão utilizadas para a configuração da execução do código.
    A lógica de leitura de cada chave no nó principal do json estará separada em métodos. Estas lógicas serão disparadas
    pelo método principal (Load).
    """

    def __init__(self, config_path: str):
        try:
            with open(config_path, mode='r') as json_config:
                self.config = json.load(json_config)
        except FileNotFoundError as file_not_found_error:
            raise ExecutionConfigurationLoadError(f"Arquivo de configuracao não foi encontrado")

    def load_config(self):
        try:
            self.load_logger_config()
            self.load_storage_config()
            self.load_scraper_config()
            # self.load_database_config()

        # todo importar modulo de tratamento de erros
        except AssertionError as assert_error:
            raise ExecutionConfigurationLoadError(f"{assert_error}")
        except KeyError as key_error:
            raise ExecutionConfigurationLoadError(f"Erro de busca de config: {key_error}")
        except RuntimeError as run_time_error:
            raise ExecutionConfigurationLoadError(f"Erro de especificação de config: {run_time_error}")

    def load_storage_config(self):
        storage_config = self.config.get("storage", None)
        if storage_config:
            data_extension = storage_config.get("dataExtension")
            if data_extension:
                os.environ["STORAGE_DATA_EXTENSION"] = data_extension
            else:
                os.environ["STORAGE_DATA_EXTENSION"] = "CSV"

            encoding = storage_config.get("encoding")
            if encoding:
                os.environ["STORAGE_DATA_ENCODING"] = encoding
            else:
                os.environ["STORAGE_DATA_ENCODING"] = "utf-8"

            local_path = storage_config.get("localPath")
            if local_path:
                os.environ["STORAGE_LOCAL_PATH"] = local_path
            else:
                os.environ["STORAGE_LOCAL_PATH"] = "/tmp/"

            storage_engine = storage_config.get("storageEngine")
            if storage_engine:
                os.environ["STORAGE_ENGINE"] = storage_engine
            else:
                os.environ["STORAGE_ENGINE"] = "csvGenerator"

        else:

            os.environ["STORAGE_LOCAL_PATH"] = "/tmp/"
            os.environ["STORAGE_DATA_EXTENSION"] = "CSV"
            os.environ["STORAGE_DATA_ENCODING"] = "utf-8"

    def load_logger_config(self):
        # todo definir o padrao de formato
        logger_config = self.config.get("logger")
        if logger_config:
            logger_format = logger_config.get("format")
            if logger_format:
                os.environ["LOGGER_FORMAT"] = logger_format
            else:
                os.environ["LOGGER_FORMAT"] = ""

            logger_level = logger_config.get("level")
            if logger_level:
                os.environ["LOGGER_LEVEL"] = logger_level
            else:
                os.environ["LOGGER_LEVEL"] = "INFO"

            logger_storage_active = logger_config.get("storage").get("active")
            if logger_storage_active:
                logger_storage_path = logger_config.get("storage").get("local").get("path")
                if logger_storage_path:
                    os.environ["LOGGER_STORAGE_PATH"] = logger_storage_path
                else:
                    os.environ["LOGGER_STORAGE_PATH"] = "/tmp/"
        else:

            os.environ["LOGGER_LEVEL"] = "INFO"
            os.environ["LOGGER_FORMAT"] = ""
            os.environ["LOGGER_STORAGE_PATH"] = "/tmp/"

    def load_scraper_config(self):
        scraper_config = self.config.get("scraper")

        if scraper_config:
            request_timeout = scraper_config.get("requestTimeout")
            if request_timeout:
                os.environ["SCRAPER_REQUEST_TIMEOUT"] = str(request_timeout)
            else:
                os.environ["SCRAPER_REQUEST_TIMEOUT"] = "30"

            max_retries = scraper_config.get("maxRetries")
            if max_retries:
                os.environ["SCRAPER_MAX_RETRIES"] = str(max_retries)
            else:
                os.environ["SCRAPER_MAX_RETRIES"] = "3"

            scraper_engine = scraper_config.get("scraperEngine")
            assert scraper_engine is not None, "É necessario informar o modulo de extração que será executado"
            os.environ["SCRAPER_ENGINE"] = scraper_engine
        else:
            raise RuntimeError("É obrigatorio configurar a execução do scraper")

    def load_database_config(self):
        # todo terminar definicoes de configuracao de database
        pass

    def get_environ_keys(self) -> list:
        return [
            "STORAGE_S3_BUCKET",
            "STORAGE_S3_KEY",
            "STORAGE_S3_ACCESS_KEY",
            "STORAGE_S3_SECRET_KEY",
            "STORAGE_S3_ACCESS_DENNY_PATH",
            "STORAGE_LOCAL_PATH",
            "STORAGE_DATA_EXTENSION",
            "STORAGE_DATA_ENCODING",
            "LOGGER_LEVEL",
            "LOGGER_FORMAT",
            "LOGGER_STORAGE_PATH",
            "SCRAPER_MAX_RETRIES",
            "SCRAPER_REQUEST_TIMEOUT",
            "SCRAPER_ENGINE"
        ]
