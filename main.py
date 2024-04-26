from time import sleep
import requests
from bs4 import BeautifulSoup
from utils import json_, print
from config import products_json_path, sample_path
from product import Product

BASE_URL = 'https://www.flulook.com.br/loja/busca.php?loja=809533'


def load_products_json():
    return json_(products_json_path) or {}


def write_products_json(products_dict):
    json_(products_json_path, products_dict, backup=True,
          n_backups=3, ensure_ascii=False, indent=2)


def load_sample():
    with open(sample_path) as f:
        return BeautifulSoup(f, 'html.parser')


def test():
    item = (load_sample())
    product = Product(item)


def get_all_by_key(key: str):
    products = load_products_json()
    return list({p[key] for p in products})


def get_products_quantity():
    products = load_products_json()
    return len(products)


def scrape():

    def color(items):
        return 'bright_green' if items else 'white'

    pg = 1
    products_dict = load_products_json()
    count_products_found = 0
    count_products_new = 0
    count_products_updated = 0
    while True:
        url = f'{BASE_URL}&palavra_busca=&pg={pg}'
        print(f'\n[bright_blue]Page {pg}[/][bright_black]: {url}')
        pg += 1
        res = requests.get(url)
        sleep(1)
        if not res.ok:
            print(f'[black on yellow]Unable to get page {url}\nAborting...')
            return
        page = BeautifulSoup(res.content, 'html.parser')
        items = page.select('li.item.flex')
        count_products_found += len(items)
        if not items:
            print('No items were found. Stopping search...')
            break
        products = [Product(item) for item in items]
        products = {p.id: p.to_dict() for p in products}
        products_new = [
            p_id for p_id in products
            if p_id not in products_dict]
        products_updated = [
            p_id for p_id in products
            if p_id in products_dict and products[p_id] != products_dict[p_id]]
        count_products_new += len(products_new)
        count_products_updated += len(products_updated)
        print(
            f'{len(items)} items -> [{color(products_new)}]{len(products_new)} new products[/] | [{color(products_updated)}]{len(products_updated)} updated products')
        products_dict.update(products)

        # for tests
        if pg > 3:
            pass
            # break

    write_products_json(products_dict)

    print(
        f'\nSearch results:'
        f'\n[bright_blue]{count_products_found}[/] total items'
        f'\n[bright_green]{count_products_new}[/] new products'
        f'\n[purple]{count_products_updated}[/] updated products'
    )


def main():
    scrape()


if __name__ == '__main__':
    main()
