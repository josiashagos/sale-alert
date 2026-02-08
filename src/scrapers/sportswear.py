"""Scrapers for sportswear and athletic brands."""

from .base import BaseScraper


class NikeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Nike Herr",
            base_url="https://www.nike.com/se/w/herr-nik1",
            sale_path="/se/w/herr-rea-3yaepznik1",
        )


class AdidasScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Adidas Herr",
            base_url="https://www.adidas.se/man",
            sale_path="/man-outlet",
        )


class NewBalanceScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="New Balance",
            base_url="https://www.newbalance.se/sv/men",
            sale_path="/sv/men/sale",
        )


SPORTSWEAR_SCRAPERS = [NikeScraper, AdidasScraper, NewBalanceScraper]
