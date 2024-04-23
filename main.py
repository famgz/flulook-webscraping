import requests
from bs4 import BeautifulSoup
from famgz_utils import json_
from pathlib import Path

source_dir = Path(__file__).parent.resolve()
json_path = Path(source_dir, 'data', 'products.json')
sample_path = Path(source_dir, 'product-sample.html')

if not json_path.exists():
     json_(json_path, {})

products = json_(json_path)

base_url = 'https://www.flulook.com.br/loja/busca.php?loja=809533&pg=1'


def parse_items(items):
    return items


def load_sample():
    with open(sample_path) as f:
        return BeautifulSoup(f, 'lxml')


def test():
    print(load_sample())


def main():
    res = requests.get(base_url)
    page = BeautifulSoup(res.content, 'lxml')
    items = page.select('li.item.flex')
    print(len(items))


if __name__ == '__main__':
    test()

    