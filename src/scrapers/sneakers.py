"""Scrapers for sneaker and streetwear stores."""

from .base import BaseScraper


class SneakersnstuffScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Sneakersnstuff",
            base_url="https://www.sneakersnstuff.com/sv",
            sale_path="/sv/sale",
        )


class FootishScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Footish",
            base_url="https://www.footish.se",
            sale_path="/rea",
        )


class SoleboxScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Solebox",
            base_url="https://www.solebox.com/en",
            sale_path="/en/sale",
        )


SNEAKER_SCRAPERS = [SneakersnstuffScraper, FootishScraper, SoleboxScraper]
