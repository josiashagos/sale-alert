"""Scrapers for premium/designer stores."""

from .base import BaseScraper


class ENDClothingScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="END Clothing",
            base_url="https://www.endclothing.com/se",
            sale_path="/se/sale",
        )


class MrPorterScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Mr Porter",
            base_url="https://www.mrporter.com/en-se/mens",
            sale_path="/en-se/mens/sale",
        )


class SSENSEScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="SSENSE",
            base_url="https://www.ssense.com/en-se/men",
            sale_path="/en-se/men/sale",
        )


class MatchesScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Matches",
            base_url="https://www.matchesfashion.com/mens",
            sale_path="/mens/sale",
        )


# Note: Louis Vuitton removed - they never have public sales
PREMIUM_SCRAPERS = [
    ENDClothingScraper,
    MrPorterScraper,
    SSENSEScraper,
    MatchesScraper,
]
