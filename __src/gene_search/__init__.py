from .gene_page_search import NCBIGeneScrapper
from bs4 import BeautifulSoup


def get_gene_name(gene_search: NCBIGeneScrapper) -> str:
    soup = BeautifulSoup(gene_search.get_page_source(), 'html.parser')
    return soup.find('td', attrs={'data-header': 'gene_name'}).text


def get_gene_symbol(gene_search: NCBIGeneScrapper) -> str:
    soup = BeautifulSoup(gene_search.get_page_source(), 'html.parser')
    return soup.find('td', attrs={'data-header': 'symbol'}).text
