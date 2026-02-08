"""Scrapers for Swedish online retailers."""

from .base import BaseScraper


class BooztScraper(BaseScraper):
    """Scraper for Boozt Men's sale page."""

    def __init__(self):
        super().__init__(
            name="Boozt Men",
            sale_url="https://www.boozt.com/se/sv/herr/rea",
            keywords=["rea", "rabatt", "% rabatt"],
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

        products = soup.select(".product-card, .product-tile, [data-product-id]")
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "REA active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class ZalandoScraper(BaseScraper):
    """Scraper for Zalando Men's sale page."""

    def __init__(self):
        super().__init__(
            name="Zalando Men",
            sale_url="https://www.zalando.se/herr-rea/",
            keywords=["rea", "rabatt", "% rabatt"],
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

        # Zalando specific selectors
        products = soup.select(
            "[data-testid='product-card'], .z-nvg-cognac-grid-item, .cat_card"
        )
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "REA active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class CalirootsScraper(BaseScraper):
    """Scraper for Caliroots sale page."""

    def __init__(self):
        super().__init__(
            name="Caliroots",
            sale_url="https://caliroots.com/sale",
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


class TresBienScraper(BaseScraper):
    """Scraper for Tres Bien sale page."""

    def __init__(self):
        super().__init__(
            name="Tres Bien",
            sale_url="https://tres-bien.com/sale",
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


SWEDISH_ONLINE_SCRAPERS = [
    BooztScraper,
    ZalandoScraper,
    CalirootsScraper,
    TresBienScraper,
]
