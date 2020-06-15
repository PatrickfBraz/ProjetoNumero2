"""
 ----
"""
from src.core.storage.storageInterface import StorageInterface
from uuid import uuid4
from os.path import join, exists
import csv
import os


class Storage(StorageInterface):
    """
    Esta classe sera usada pelo scraper para salvar o resultado das extrações num arquivo csv local.

    IMPORTANTE:
        Os métodos de escrita desta classe utilizam o dictWriter. Em outras palavras, os records passados não devem
        possuir colunas com diferentes nomes. Caso isto ocorra, pode ser que sejam disparadas exceções ocasionando o
        mau funcionamento da classe.
    """

    def __init__(self, logger=None):
        super().__init__(logger=logger)
        self._csv_name = str(uuid4()) + ".csv"
        self._file_path = join(self.local_path, self._csv_name)
        self.delimeter = ';'
        try:
            if not exists(self._file_path):
                with open(self._file_path, 'w', encoding=self.data_encoding): pass
        except FileNotFoundError as error:
            self.logger.critical(
                f"Não foi possivel criar o arquivo csv no caminho {self._file_path}")
            # todo determinar qual excecao disparar

    def set_csv_name(self, name: str):
        self._csv_name = name

    def save_record(self, record: dict):
        columns = list(record.keys())
        # todo utilizar o dict writer
        if os.path.getsize(self._file_path) <= 1:
            with open(self._file_path, 'w', newline='', encoding=self.data_encoding) as csv_file:
                # se o arquivo nao possui conteudo
                file_writer = csv.DictWriter(csv_file, fieldnames=columns)
                file_writer.writeheader()
                file_writer.writerow(record)
        else:
            with open(self._file_path, 'a', newline='', encoding=self.data_encoding) as csv_file:
                # se ja existe conteudo no arquivo
                file_writer = csv.DictWriter(csv_file, fieldnames=columns)
                file_writer.writerow(record)

    def save_record_batch(self, records: list):
        columns = list(records[0].keys())
        # todo utilizar o dict writer
        if os.path.getsize(self._file_path) <= 1:
            with open(self._file_path, 'w', newline='', encoding=self.data_encoding) as csv_file:
                # se o arquivo nao possui conteudo
                file_writer = csv.DictWriter(csv_file, fieldnames=columns)
                file_writer.writeheader()
                for record in records:
                    file_writer.writerow(record)
        else:
            with open(self._file_path, 'a', newline='', encoding=self.data_encoding) as csv_file:
                # se ja existe conteudo no arquivo
                file_writer = csv.DictWriter(csv_file, fieldnames=columns)
                for record in records:
                    file_writer.writerow(record)
