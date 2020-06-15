"""
Modulo responsável por conter toda a lógica de busca e extracao dos dados.

A classe de extracao de dados é capaz de lidar com a busca, porêm não com o tratamento dos dados. Por isso, esta classe
se comunica com a classe responsável por tratar e salvar os dados encontrada no sub modulo src.storage
"""
from bs4 import BeautifulSoup
from src.core.scraper.httpScraperAbstract import HttpScraperAbstract, http_scraper_execution_timer
from requests import get
from src.error.error_types import ScraperExecutionError
import re


class HttpScraper(HttpScraperAbstract):
    """

    """

    def __init__(self, logger=None):
        super().__init__(logger)
        self.source_url = "http://books.toscrape.com/"
        self.regex_monetary_pattern = re.compile("[\d\.]+(,|.)\d+")

    @http_scraper_execution_timer
    def execute(self):
        self.logger.info(f"Iniciando execucao do scraper {self.module_name}")
        self.get_execution_description()

        self.make_request(request_method=get, url=self.source_url)

        if self.current_request:
            navigator = self.get_menu_navigator(self.current_request.text)
            for endpoint in navigator:
                self.logger.debug(f"Acessando: {self.source_url + endpoint[0]}")

                self.make_request(url=(self.source_url + endpoint[0]), request_method=get)
                next_pages = self.find_next_pages(self.current_request.text)
                self.extrac_books_info(category=endpoint[1], html_string=self.current_request.text)

                for new_page in next_pages:
                    self.make_request(url=(self.source_url + endpoint[0].replace("index.html", new_page)),
                                      request_method=get)
                    self.extrac_books_info(category=endpoint[1], html_string=self.current_request.text)
        else:
            self.logger.critical(f"Não foi possivel acessar a fonte {self.source_url}.")
            raise ScraperExecutionError(f"Ocorreu algum erro ao tebtar acessar a fonte: {self.source_url}")

    def get_execution_description(self):
        self.logger.info("Fonte dos dados: http://books.toscrape.com/")

    def get_menu_navigator(self, html_string: str) -> list:
        """
        Este metodo retorna uma lista de tuplas contendo as url e a string que representa o gênero do livro. As url
        serão usadas para buscar os conteúdos das páginas.
        """
        try:
            links = []
            html_parser = BeautifulSoup(html_string, 'html.parser')
            menu = html_parser.aside.find_all("div")[1].find_all('a')[1:]

            for element in menu:
                links.append((element.get('href'), element.text.strip()))
            return links
        except ValueError as error:
            self.logger.critical(f"Erro de execucao: {error}")
            raise ScraperExecutionError(f"{error}")

    @staticmethod
    def find_next_pages(html_string: str) -> list:
        html_parser = BeautifulSoup(html_string, 'html.parser')
        next_pages = list()
        section = html_parser.section
        next_page_li = section.find_all("li")
        for li in next_page_li:
            if li.a and li.a.string:
                if li.a.string.upper() == "NEXT":
                    next_pages.append(li.a.get('href'))
        return next_pages

    def extrac_books_info(self, category: str, html_string: str):
        star_rating = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        try:
            html_parser = BeautifulSoup(html_string, 'html.parser')
            book_list = html_parser.section.find_all("article")
            book_attributes = {
                "category": category
            }
            for element in book_list:
                book_attributes["rating"] = star_rating.get(element.p["class"][1])
                book_attributes["title"] = element.h3.a.string
                book_attributes["price"] = element.find_all("div")[1].p.string.replace("£", " ").split(" ")[1]
                book_attributes["stock_info"] = element.find_all("div")[1].find_all("p")[1].i["class"][0].split("-")[-1]
                self.storage_interface.save_record(record=book_attributes)

        except ValueError as error:
            self.logger.critical(f"Erro de execucao: {error}")
            raise ScraperExecutionError(f"{error}")
