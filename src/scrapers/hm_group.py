"""Scrapers for H&M Group stores (H&M, COS, Arket, Weekday)."""

from .base import BaseScraper


class HMScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="H&M Herr",
            base_url="https://www2.hm.com/sv_se/herr.html",
            sale_path="/sv_se/herr/rea.html",
        )


class COSScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="COS Herr",
            base_url="https://www.cos.com/sv-se/men.html",
            sale_path="/sv-se/men/sale.html",
        )


class ArketScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Arket Herr",
            base_url="https://www.arket.com/sv-se/men.html",
            sale_path="/sv-se/men/sale.html",
        )


class WeekdayScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="Weekday Herr",
            base_url="https://www.weekday.com/sv-se/men.html",
            sale_path="/sv-se/men/sale.html",
        )


HM_GROUP_SCRAPERS = [HMScraper, COSScraper, ArketScraper, WeekdayScraper]
