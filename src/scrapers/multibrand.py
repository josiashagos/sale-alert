"""Scrapers for multi-brand retailers."""

from .base import BaseScraper


class CareOfCarlScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Care of Carl",
            base_url="https://www.careofcarl.se/sv",
            sale_path="/sv/sale",
        )


MULTIBRAND_SCRAPERS = [CareOfCarlScraper]
