"""Scrapers for Inditex group and similar fast fashion (Zara, Mango, Massimo Dutti, Uniqlo)."""

from .base import BaseScraper


class ZaraScraper(BaseScraper):
    """Scraper for Zara Man sale page."""

    def __init__(self):
        super().__init__(
            name="Zara Man",
            sale_url="https://www.zara.com/se/sv/man-sale-l806.html",
            keywords=["sale", "rea", "% off"],
            use_playwright=True,  # Zara is heavily JavaScript-based
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

        # Zara specific selectors
        products = soup.select(
            ".product-grid__product, .product-grid-item, [data-productid]"
        )
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


class MangoScraper(BaseScraper):
    """Scraper for Mango Man sale page."""

    def __init__(self):
        super().__init__(
            name="Mango Man",
            sale_url="https://shop.mango.com/se/man/sale",
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

        # Mango specific selectors
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


class UniqloScraper(BaseScraper):
    """Scraper for Uniqlo Men sale page."""

    def __init__(self):
        super().__init__(
            name="Uniqlo Men",
            sale_url="https://www.uniqlo.com/se/en/men/sale",
            keywords=["sale", "limited offer", "special price"],
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

        # Uniqlo specific selectors
        products = soup.select(".fr-ec-product-tile, .product-tile, [data-product-id]")
        has_products = len(products) > 0

        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or "Limited offers available",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class MassimoDuttiScraper(BaseScraper):
    """Scraper for Massimo Dutti Men sale page."""

    def __init__(self):
        super().__init__(
            name="Massimo Dutti Men",
            sale_url="https://www.massimodutti.com/se/men/sale-n1805",
            keywords=["sale", "rea"],
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

        products = soup.select(".product-grid-item, .product-card, [data-productid]")
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


INDITEX_SCRAPERS = [ZaraScraper, MangoScraper, UniqloScraper, MassimoDuttiScraper]
