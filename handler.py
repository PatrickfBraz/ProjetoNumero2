"""
Este módulo contem a função principal responsável por coordenar as demais chamadas de módulos.
"""
from src.settings.configLoader import ConfigLoader
from src.error.error_types import *
from src.logger.loggerConfig import CustomLogger
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
        ConfigLoader().load_config()

        logger = CustomLogger().get_logger()
        logger.debug("Logger Iniciado")

        logger.debug("Verificando configurações de ambiente carregadas")
        for key, value in os.environ:
            if key.find("LOGGER") >= 0 or key.find("STORAGE") >= 0 or key.find("SCRAPER") >= 0:
                logger.debug("{key} = {value}".format_map({"key": key, "value": value}))

        logger.info("Fazendo chamada para o scrapper")
        # todo implementar scraper

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
