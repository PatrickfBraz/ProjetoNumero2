"""
Este documento define todas as classes de erros que serão disparadas pela aplicação
"""


class ExecutionConfigurationLoadError(BaseException):
    """
    Objeto responsavel por explicitar uma exceção disparada no carregamento das configurações de execução
    """

    def __init__(self, message: str = ""):
        super().__init__(message)


class ScraperExecutionError(BaseException):
    """
    Objeto responsavel por explicitar uma exceção disparada na execução do scraper
    """

    def __init__(self, message: str = ""):
        super().__init__(message)


class LoggerGenerationError(BaseException):
    """
    Objeto responsavel por explicitar uma exceção disparada na criação do logger
    """

    def __init__(self, message: str = ""):
        super().__init__(message)
