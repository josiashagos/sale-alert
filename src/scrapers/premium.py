"""Scrapers for premium/designer stores."""

from .base import BaseScraper


class ENDClothingScraper(BaseScraper):
    """Scraper for END. Clothing sale page."""

    def __init__(self):
        super().__init__(
            name="END Clothing",
            sale_url="https://www.endclothing.com/se/sale",
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

        products = soup.select(".ProductCard, .product-card, [data-testid='product']")
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


class LouisVuittonScraper(BaseScraper):
    """Scraper for Louis Vuitton - note: LV rarely has sales."""

    def __init__(self):
        super().__init__(
            name="Louis Vuitton",
            sale_url="https://eu.louisvuitton.com/swe-se/men/_/N-t15mfk3d",
            keywords=["sale", "special"],
            use_playwright=True,
        )

    def check_sale(self) -> dict:
        # LV rarely has public sales, so we mainly check for any special offers
        html = self.fetch_page()
        if not html:
            return {
                "active": False,
                "store_name": self.name,
                "url": self.sale_url,
                "error": "Failed to fetch page",
            }

        soup = self.parse_html(html)
        has_sale, description = self.has_sale_indicators(soup)

        if has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Special offer available",
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class MrPorterScraper(BaseScraper):
    """Scraper for Mr Porter sale page."""

    def __init__(self):
        super().__init__(
            name="Mr Porter",
            sale_url="https://www.mrporter.com/en-se/mens/sale",
            keywords=["sale", "% off", "reduced"],
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

        products = soup.select(".ProductItem, .product-card, [data-product]")
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


class SSENSEScraper(BaseScraper):
    """Scraper for SSENSE sale page."""

    def __init__(self):
        super().__init__(
            name="SSENSE",
            sale_url="https://www.ssense.com/en-se/men/sale",
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

        products = soup.select(".product-tile, .plp-product, [data-product-id]")
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


class MatchesScraper(BaseScraper):
    """Scraper for Matches Fashion sale page."""

    def __init__(self):
        super().__init__(
            name="Matches",
            sale_url="https://www.matchesfashion.com/mens/sale",
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

        products = soup.select(".ProductCard, .product-card, [data-product]")
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


PREMIUM_SCRAPERS = [
    ENDClothingScraper,
    LouisVuittonScraper,
    MrPorterScraper,
    SSENSEScraper,
    MatchesScraper,
]
