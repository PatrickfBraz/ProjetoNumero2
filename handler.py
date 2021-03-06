"""
Este módulo contem a função principal responsável por coordenar as demais chamadas de módulos.
"""
from src.settings.configLoader import ConfigLoader
from src.error.error_types import *
from src.logger.loggerConfig import CustomLogger
from src.core.scraper.httpScraperAbstract import initialize_scraper_engine
import os
import time
import json
import sys


def handler(event=None, context=None):
    """
    Função principal que dispara a execução do scraper segundo os parâmetros de configuração.

    Como esta função foi criada para ser compativel com o AWS Lambda, ela recebe dois parâmetros de entrada, os quais
    representam o evento recebido e o contexto de execução da função.

    Estes parâmetros não são obrigatórios para a execução, mas permitem a integração com o AWS Lambda.

    :param event: dict (Não obrigatorio) evento que dispara a execução
    :param context: object (Não obrigatorio) contexto da execução
    :return: Não possui retorno definido
    """
    try:
        loader = ConfigLoader("./src/settings/parameters.json")
        loader.load_config()
        logger = CustomLogger().get_logger()
        logger.info("Logger Iniciado")
        logger.info("Verificando configurações de ambiente carregadas")
        for key in loader.get_environ_keys():
            if os.environ.get(key, None):
                value = os.environ.get(key)
                logger.debug("{key} = {value}".format_map({"key": key, "value": value}))

        logger.info("Fazendo chamada para o scraper")
        # todo implementar scraper
        initialize_scraper_engine(logger=logger)
        logger.info("Handler executado com sucesso!")
        return

    except ExecutionConfigurationLoadError as load_config_error:
        # A mensagem é mostrada desta forma pois o logger só é definido após carregamento das configurações
        message = {
            "timestamp": time.time(),
            "level": "CRITICAL",
            "location": "handler",
            "message": f"{load_config_error}"
        }
        print(json.dumps(message))
        sys.exit(1)
