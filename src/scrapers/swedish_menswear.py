"""Scrapers for Swedish menswear brands."""

from .base import BaseScraper


class GrandpaScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Grandpa",
            base_url="https://www.grandpastore.com/se",
            sale_path="/se/sale",
        )


class EtonScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="ETON",
            base_url="https://www.etonshirts.com/se",
            sale_path="/se/sale",
        )


class OscarJacobsonScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Oscar Jacobson",
            base_url="https://www.oscarjacobson.com/se",
            sale_path="/se/sale",
        )


class TigerOfSwedenScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Tiger of Sweden",
            base_url="https://www.tigerofsweden.com/se/herr",
            sale_path="/se/sale/herr",
        )


class RalphLaurenScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Ralph Lauren",
            base_url="https://www.ralphlauren.se/sv/herr",
            sale_path="/sv/sale/herr",
        )


class BrixtolTextilesScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Brixtol Textiles",
            base_url="https://www.brixtoltextiles.com",
            sale_path="/sale",
        )


SWEDISH_MENSWEAR_SCRAPERS = [
    GrandpaScraper,
    EtonScraper,
    OscarJacobsonScraper,
    TigerOfSwedenScraper,
    RalphLaurenScraper,
    BrixtolTextilesScraper,
]
