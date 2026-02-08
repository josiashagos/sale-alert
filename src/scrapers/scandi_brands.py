"""Scrapers for Scandinavian fashion brands."""

from .base import BaseScraper


class OurLegacyScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Our Legacy",
            base_url="https://www.ourlegacy.com",
            sale_path="/sale",
        )


class SamsoeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Samsøe Samsøe",
            base_url="https://www.samsoe.com/sv/man",
            sale_path="/sv/man/sale",
        )


class AcneStudiosScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Acne Studios",
            base_url="https://www.acnestudios.com/se/en/man",
            sale_path="/se/en/man/sale",
        )


class NorseProjectsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Norse Projects",
            base_url="https://www.norseprojects.com/store/men",
            sale_path="/store/men/sale",
        )


class NN07Scraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="NN07",
            base_url="https://www.nn07.com/se/men",
            sale_path="/se/men/sale",
        )


SCANDI_SCRAPERS = [
    OurLegacyScraper,
    SamsoeScraper,
    AcneStudiosScraper,
    NorseProjectsScraper,
    NN07Scraper,
]
