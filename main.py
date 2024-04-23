from time import sleep
import requests
from bs4 import BeautifulSoup
from utils import json_, print
from config import products_json_path, sample_path
from product import Product

BASE_URL = 'https://www.flulook.com.br/loja/busca.php?loja=809533'


def load_products_json():
    return json_(products_json_path) or []


def write_products_json(products_list):
    json_(products_json_path, products_list, ensure_ascii=False, indent=2)


def load_sample():
    with open(sample_path) as f:
        return BeautifulSoup(f, 'lxml')


def test():
    item = (load_sample())
    product = Product(item)


def scrape():
    pg = 1
    products_list = load_products_json()
    count_products_found = 0
    count_products_new = 0
    while True:
        url = f'{BASE_URL}&palavra_busca=&pg={pg}'
        print(f'[bright_blue]Page {pg}[/][bright_black]: {url}')
        pg += 1
        res = requests.get(url)
        sleep(1)
        if not res.ok:
            print(f'[black on yellow]Unable to get page {url}\nAborting...')
            return
        page = BeautifulSoup(res.content, 'lxml')
        items = page.select('li.item.flex')
        count_products_found += len(items)
        if not items:
            print('No items were found. Exiting...')
            break
        products = [Product(item).to_dict() for item in items]
        products_new = [x for x in products if x not in products_list]
        count_products_new += len(products_new)
        print(f'{len(items)} items -> [bright_green]{len(products)} new products')
        if not products_new:
            continue
        products_list += products_new
        write_products_json(products_list)
        # break
    
    print(f'\nSearch finished with [bright_blue]{count_products_found} items[/] and [purple]{count_products_new} new products')


def main():
    scrape()


if __name__ == '__main__':
    main()
