"""Scrapers for Swedish department stores."""

from .base import BaseScraper


class NKScraper(BaseScraper):
    """Scraper for NK (Nordiska Kompaniet) Herr sale page."""

    def __init__(self):
        super().__init__(
            name="NK Herr",
            sale_url="https://www.nk.se/herr/rea",
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


class AhlensScraper(BaseScraper):
    """Scraper for Åhléns Herr sale page."""

    def __init__(self):
        super().__init__(
            name="Ahlens Herr",
            sale_url="https://www.ahlens.se/mode/herr/rea/",
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

        products = soup.select(".product-card, .product-item, [data-product-id]")
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


DEPARTMENT_SCRAPERS = [NKScraper, AhlensScraper]
