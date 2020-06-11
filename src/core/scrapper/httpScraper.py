"""
Modulo responsável por conter toda a lógica de busca e extracao dos dados.

A classe de extracao de dados é capaz de lidar com a busca, porêm não com o tratamento dos dados. Por isso, esta classe
se comunica com a classe responsável por tratar e salvar os dados encontrada no sub modulo src.storage
"""
from bs4 import BeautifulSoup
from requests import get, post, put


class HttpScraper:
    """

    """
    def __init__(self):
        pass