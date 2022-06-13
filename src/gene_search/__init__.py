from .gene_page_search import GenePageSearch
from bs4 import BeautifulSoup


def get_gene_name(gene_search: GenePageSearch) -> str:
    soup = BeautifulSoup(gene_search.get_page_source(), 'html.parser')
    return soup.find('td', attrs={'data-header': 'gene_name'}).text
