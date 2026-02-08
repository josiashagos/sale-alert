"""Scrapers for sportswear and athletic brands."""

from .base import BaseScraper


class NikeScraper(BaseScraper):
    """Scraper for Nike Sweden sale page."""

    def __init__(self):
        super().__init__(
            name="Nike",
            sale_url="https://www.nike.com/se/w/mens-sale-3yaepznik1",
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
        products = soup.select(".product-card, .product-grid__item, [data-testid='product-card']")
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


class AdidasScraper(BaseScraper):
    """Scraper for Adidas Sweden sale page."""

    def __init__(self):
        super().__init__(
            name="Adidas",
            sale_url="https://www.adidas.se/man-outlet",
            keywords=["sale", "rea", "outlet", "% off"],
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
        products = soup.select(".product-card, .plp-grid__item, [data-testid='product-card']")
        has_products = len(products) > 0
        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Outlet active",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class NewBalanceScraper(BaseScraper):
    """Scraper for New Balance Sweden sale page."""

    def __init__(self):
        super().__init__(
            name="New Balance",
            sale_url="https://www.newbalance.se/en/men/sale/",
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


SPORTSWEAR_SCRAPERS = [NikeScraper, AdidasScraper, NewBalanceScraper]
