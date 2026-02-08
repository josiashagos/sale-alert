"""Scrapers for Swedish department stores."""

from .base import BaseScraper


class NKScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="NK Herr",
            base_url="https://www.nk.se/herr",
            sale_path="/herr/rea",
        )


class AhlensScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Åhléns Herr",
            base_url="https://www.ahlens.se/mode/herr",
            sale_path="/mode/herr/rea",
        )


DEPARTMENT_SCRAPERS = [NKScraper, AhlensScraper]
