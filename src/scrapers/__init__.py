"""Scrapers for all fashion stores."""

from .base import BaseScraper
from .hm_group import HM_GROUP_SCRAPERS
from .inditex import INDITEX_SCRAPERS
from .scandi_brands import SCANDI_SCRAPERS
from .premium import PREMIUM_SCRAPERS
from .swedish_online import SWEDISH_ONLINE_SCRAPERS
from .department import DEPARTMENT_SCRAPERS
from .sneakers import SNEAKER_SCRAPERS
from .sportswear import SPORTSWEAR_SCRAPERS
from .swedish_menswear import SWEDISH_MENSWEAR_SCRAPERS
from .multibrand import MULTIBRAND_SCRAPERS

# Collect all scrapers
ALL_SCRAPERS = (
    HM_GROUP_SCRAPERS
    + INDITEX_SCRAPERS
    + SCANDI_SCRAPERS
    + PREMIUM_SCRAPERS
    + SWEDISH_ONLINE_SCRAPERS
    + DEPARTMENT_SCRAPERS
    + SNEAKER_SCRAPERS
    + SPORTSWEAR_SCRAPERS
    + SWEDISH_MENSWEAR_SCRAPERS
    + MULTIBRAND_SCRAPERS
)


def get_all_scrapers() -> list[BaseScraper]:
    """Instantiate and return all scrapers."""
    return [scraper_class() for scraper_class in ALL_SCRAPERS]


def get_scraper_by_name(name: str) -> BaseScraper | None:
    """Get a scraper by store name."""
    for scraper_class in ALL_SCRAPERS:
        scraper = scraper_class()
        if scraper.name.lower() == name.lower():
            return scraper
    return None


__all__ = [
    "BaseScraper",
    "get_all_scrapers",
    "get_scraper_by_name",
    "ALL_SCRAPERS",
    "HM_GROUP_SCRAPERS",
    "INDITEX_SCRAPERS",
    "SCANDI_SCRAPERS",
    "PREMIUM_SCRAPERS",
    "SWEDISH_ONLINE_SCRAPERS",
    "DEPARTMENT_SCRAPERS",
    "SNEAKER_SCRAPERS",
    "SPORTSWEAR_SCRAPERS",
    "SWEDISH_MENSWEAR_SCRAPERS",
    "MULTIBRAND_SCRAPERS",
]
