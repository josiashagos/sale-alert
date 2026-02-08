"""Scrapers for sneaker and streetwear stores."""

from .base import BaseScraper


class SneakersnstuffScraper(BaseScraper):
    """Scraper for Sneakersnstuff (SNS) sale page."""

    def __init__(self):
        super().__init__(
            name="Sneakersnstuff",
            sale_url="https://www.sneakersnstuff.com/en/sale",
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

        products = soup.select(".product-card, .product-item, [data-product-id]")
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


class FootishScraper(BaseScraper):
    """Scraper for Footish sale page."""

    def __init__(self):
        super().__init__(
            name="Footish",
            sale_url="https://www.footish.se/rea",
            keywords=["rea", "sale", "% rabatt"],
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
                "description": description or "REA active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class SoleboxScraper(BaseScraper):
    """Scraper for Solebox sale page."""

    def __init__(self):
        super().__init__(
            name="Solebox",
            sale_url="https://www.solebox.com/en/sale/",
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

        products = soup.select(".product-card, .product-tile, [data-product-id]")
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


SNEAKER_SCRAPERS = [SneakersnstuffScraper, FootishScraper, SoleboxScraper]
