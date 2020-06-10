from src.settings.configLoader import ConfigLoader


def handler(event=None, context=None):
    """
    Função principal que dispara a execução do scraper segundo os parâmetros de configuração
    :param event: --
    :param context: --
    :return:
    """
    try:
        ConfigLoader.load_config()
        # todo carrega as configuracoes
        # todo carrega o logger
        # todo chama o scraper
        # todo chama o storage interface
        # todo chama o database interface
    except ValueError as value_error:
        # todo criar modulo de tratamento de erro
        pass

