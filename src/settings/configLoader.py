class ConfigLoader:
    """
    Esta classe é responsável por ler o arquivo de parametros de execução e criar as variaveis de ambiente as quais
    serão utilizadas para a configuração da execução do código.
    A lógica de leitura de cada chave no nó principal do json estará separada em métodos. Estas lógicas serão disparadas
    pelo método principal (Load).
    """

    def __init__(self):
        pass

    def load(self):
        pass

    def load_storage_config(self):
        pass

    def load_logger_config(self):
        pass

    def load_scraper_config(self):
        pass

    def load_database_config(self):
        pass
