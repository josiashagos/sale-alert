"""Scrapers for Swedish online retailers."""

from .base import BaseScraper


class BooztScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Boozt Herr",
            base_url="https://www.boozt.com/se/sv/herr",
            sale_path="/se/sv/herr/rea",
        )


class ZalandoScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Zalando Herr",
            base_url="https://www.zalando.se/herr-home/",
            sale_path="/herr-rea/",
        )


class CalirootsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Caliroots",
            base_url="https://caliroots.com",
            sale_path="/sale",
        )


class TresBienScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Très Bien",
            base_url="https://tres-bien.com",
            sale_path="/sale",
        )


SWEDISH_ONLINE_SCRAPERS = [
    BooztScraper,
    ZalandoScraper,
    CalirootsScraper,
    TresBienScraper,
]
