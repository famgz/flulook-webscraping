from bs4 import BeautifulSoup
from pathlib import Path
from famgz_utils import print
from config import debug_dir


class Product:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup  # <li class="item flex">
        self.id = self.get_id()
        self.brand = self.get_brand()
        self.model = self.get_model()
        self.fullName = self.get_fullName()
        self.url = self.get_url()
        self.category = self.get_category()
        self.slug = self.get_slug()
        self.price = self.get_price()
        self.imgUrl = self.get_imgUrl()

    def log_debug(self):
        debug_path = Path(debug_dir, f'{self.id}.html')
        if debug_path.exists():
            return
        with open(debug_path, 'w') as f:
            f.write(self.soup.prettify())

    def get_id(self):
        return self.soup.select_one('li > div[data-id]')['data-id']

    def get_brand(self):
        try:
            return self.soup.select_one('div[itemprop="brand"]').select_one('span').get_text(strip=True)
        except AttributeError:
            self.log_debug()
            return None

    def get_model(self):
        try:
            return self.soup.select_one('span[itemprop="model"]').get_text(strip=True)
        except AttributeError:
            self.log_debug()
            return None

    def get_fullName(self):
        return self.soup.select_one('img[itemprop="image"]')['alt']
    
    def get_url(self):
        return self.soup.select_one('a[itemprop="url"]')['href']
    
    def get_category(self):
        if not self.url:
            return None
        return self.url.strip('/').split('/')[-2]
    
    def get_slug(self):
        if not self.url:
            return None
        return self.url.strip('/').split('/')[-1]
    
    def get_price(self):
        return self.soup.select_one('meta[itemprop="price"]').get('content')
    
    def get_imgUrl(self):
        return self.soup.select_one('img[itemprop="image"]').get('src')


    def to_dict(self):
        return dict(
            id=self.id,
            brand=self.brand,
            model=self.model,
            fullName=self.fullName,
            category=self.category,
            slug=self.slug,
            url=self.url,
            price=self.price,
            imgUrl=self.imgUrl,
        )