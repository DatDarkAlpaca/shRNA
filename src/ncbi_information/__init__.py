from .scrapper import NCBIGeneScrapper
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class NCBIInformation:
    name: str
    symbol: str


def get_gene_name(gene_search: NCBIGeneScrapper) -> str:
    soup = BeautifulSoup(gene_search.get_page_source(), 'html.parser')
    return soup.find('td', attrs={'data-header': 'gene_name'}).text


def get_gene_symbol(gene_search: NCBIGeneScrapper) -> str:
    soup = BeautifulSoup(gene_search.get_page_source(), 'html.parser')
    return soup.find('td', attrs={'data-header': 'symbol'}).text


def get_ncbi_gene_information(driver, gene_id=None) -> NCBIInformation:
    page_search = NCBIGeneScrapper(driver, gene_id)
    name = get_gene_name(page_search)
    symbol = get_gene_symbol(page_search)

    return NCBIInformation(name, symbol)
