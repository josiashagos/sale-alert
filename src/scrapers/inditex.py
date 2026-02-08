"""Scrapers for fast fashion brands (Zara, Mango, Uniqlo, Massimo Dutti)."""

from .base import BaseScraper


class ZaraScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Zara Herr",
            base_url="https://www.zara.com/se/sv/man-l1.html",
            sale_path="/se/sv/man-special-prices-l1314.html",
        )


class MangoScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Mango Man",
            base_url="https://shop.mango.com/se/herr",
            sale_path="/se/herr/kampanjer/rea",
        )


class UniqloScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Uniqlo Herr",
            base_url="https://www.uniqlo.com/se/sv/herr",
            sale_path="/se/sv/herr/erbjudanden",
        )


class MassimoDuttiScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Massimo Dutti Herr",
            base_url="https://www.massimodutti.com/se/herr",
            sale_path="/se/herr/sale-c1866509.html",
        )


INDITEX_SCRAPERS = [ZaraScraper, MangoScraper, UniqloScraper, MassimoDuttiScraper]
