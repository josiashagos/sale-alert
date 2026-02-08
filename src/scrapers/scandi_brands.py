"""Scrapers for Scandinavian fashion brands."""

from .base import BaseScraper


class OurLegacyScraper(BaseScraper):
    """Scraper for Our Legacy sale page."""

    def __init__(self):
        super().__init__(
            name="Our Legacy",
            sale_url="https://www.ourlegacy.com/sale",
            keywords=["sale", "archive", "% off"],
            use_playwright=True,
        )

    def check_sale(self) -> dict:
        html = self.fetch_page()
        if not html:
            return {
                "active": False,
                "store_name": self.name,
                "url": self.sale_url,
                "error": "Failed to fetch page",
            }

        soup = self.parse_html(html)

        products = soup.select(".product, .product-card, .product-item")
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Archive sale active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class SamsoeScraper(BaseScraper):
    """Scraper for Samsoe Samsoe sale page."""

    def __init__(self):
        super().__init__(
            name="Samsoe Samsoe",
            sale_url="https://www.samsoe.com/sv/man/sale/",
            keywords=["sale", "rea", "% off"],
            use_playwright=True,
        )

    def check_sale(self) -> dict:
        html = self.fetch_page()
        if not html:
            return {
                "active": False,
                "store_name": self.name,
                "url": self.sale_url,
                "error": "Failed to fetch page",
            }

        soup = self.parse_html(html)

        products = soup.select(".product-card, .product-tile, [data-product]")
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Sale active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class AcneStudiosScraper(BaseScraper):
    """Scraper for Acne Studios sale page."""

    def __init__(self):
        super().__init__(
            name="Acne Studios",
            sale_url="https://www.acnestudios.com/se/en/man/sale/",
            keywords=["sale", "archive", "% off"],
            use_playwright=True,
        )

    def check_sale(self) -> dict:
        html = self.fetch_page()
        if not html:
            return {
                "active": False,
                "store_name": self.name,
                "url": self.sale_url,
                "error": "Failed to fetch page",
            }

        soup = self.parse_html(html)

        products = soup.select(".product-card, .product-tile, [data-product]")
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Sale active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class NorseProjectsScraper(BaseScraper):
    """Scraper for Norse Projects sale page."""

    def __init__(self):
        super().__init__(
            name="Norse Projects",
            sale_url="https://www.norseprojects.com/collection/men-sale",
            keywords=["sale", "% off"],
            use_playwright=True,
        )

    def check_sale(self) -> dict:
        html = self.fetch_page()
        if not html:
            return {
                "active": False,
                "store_name": self.name,
                "url": self.sale_url,
                "error": "Failed to fetch page",
            }

        soup = self.parse_html(html)

        products = soup.select(".product-card, .product-grid-item, [data-product-id]")
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Sale active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class NN07Scraper(BaseScraper):
    """Scraper for NN07 sale page."""

    def __init__(self):
        super().__init__(
            name="NN07",
            sale_url="https://www.nn07.com/en/men/sale",
            keywords=["sale", "% off"],
            use_playwright=True,
        )

    def check_sale(self) -> dict:
        html = self.fetch_page()
        if not html:
            return {
                "active": False,
                "store_name": self.name,
                "url": self.sale_url,
                "error": "Failed to fetch page",
            }

        soup = self.parse_html(html)

        products = soup.select(".product-card, .product-item, [data-product]")
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Sale active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


SCANDI_SCRAPERS = [
    OurLegacyScraper,
    SamsoeScraper,
    AcneStudiosScraper,
    NorseProjectsScraper,
    NN07Scraper,
]
