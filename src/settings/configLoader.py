import os
import json


class ConfigLoader:
    """
    Esta classe é responsável por ler o arquivo de parametros de execução e criar as variaveis de ambiente as quais
    serão utilizadas para a configuração da execução do código.
    A lógica de leitura de cada chave no nó principal do json estará separada em métodos. Estas lógicas serão disparadas
    pelo método principal (Load).
    """

    def __init__(self):
        with open(os.path.join(os.curdir, "parameters.json"), mode='r') as json_config:
            self.config = json.load(json_config)

    def load_config(self):
        try:
            self.load_logger_config()
            self.load_storage_config()
            self.load_scraper_config()
            # self.load_database_config()

        # todo importar modulo de tratamento de erros
        except AssertionError as assert_error:
            raise ValueError(assert_error)
        except KeyError as key_error:
            raise ValueError(f"Erro de busca de config: {key_error}")

    def load_storage_config(self):
        storage_config = self.config.get("storage", None)
        if storage_config:
            dataExtension = storage_config.get("dataExtension")
            if dataExtension:
                os.environ["STORAGE_DATA_EXTENSION"] = dataExtension
            else:
                os.environ["STORAGE_DATA_EXTENSION"] = "CSV"

            encoding = storage_config.get("encoding")
            if encoding:
                os.environ["STORAGE_DATA_ENCODING"] = dataExtension
            else:
                os.environ["STORAGE_DATA_ENCODING"] = "utf-8"

            remote = storage_config.get("remote")
            if remote:
                bucket = storage_config.get("s3").get("bucket")
                key = storage_config.get("s3").get("key")
                access_key = storage_config.get("s3").get("accessKey")
                secret_key = storage_config.get("s3").get("secretKey")
                localPath = storage_config.get("s3").get("acessDenyConfig").get("path")

                assert access_key is not None, "Não foi possivel carregar informaçeõs de acesso ao S3: (access_key)"
                assert secret_key is not None, "Não foi possivel carregar informaçeõs de acesso ao S3: (secret_key)"

                os.environ["STORAGE_S3_BUCKET"] = bucket
                os.environ["STORAGE_S3_KEY"] = key
                os.environ["STORAGE_S3_ACCESS_KEY"] = access_key
                os.environ["STORAGE_S3_SECRET_KEY"] = secret_key
                os.environ["STORAGE_S3_ACCESS_DENNY_PATH"] = localPath

            else:
                localPath = storage_config.get("localPath")
                if localPath:
                    os.environ["STORAGE_LOCAL_PATH"] = localPath
                else:
                    os.environ["STORAGE_LOCAL_PATH"] = "/tmp/"
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
                os.environ["SCRAPER_REQUEST_TIMEOUT"] = request_timeout
            else:
                os.environ["SCRAPER_REQUEST_TIMEOUT"] = "30"

            max_retries = scraper_config.get("maxRetries")
            if max_retries:
                os.environ["SCRAPER_MAX_RETRIES"] = max_retries
            else:
                os.environ["SCRAPER_MAX_RETRIES"] = "3"
        else:

            os.environ["SCRAPER_MAX_RETRIES"] = "3"
            os.environ["SCRAPER_REQUEST_TIMEOUT"] = "30"

    def load_database_config(self):
        # todo terminar definicoes de configuracao de database
        pass
