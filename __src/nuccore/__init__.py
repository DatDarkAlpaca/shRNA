from lxml import html
import requests


def get_nuccore_name(variant_string: str):
    page = requests.get(f"https://www.ncbi.nlm.nih.gov/nuccore/{variant_string}")
    tree = html.fromstring(page.content)

    result = tree.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/h1')
    return result[0].text if result else 'None'
