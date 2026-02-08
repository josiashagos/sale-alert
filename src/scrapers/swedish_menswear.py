"""Scrapers for Swedish menswear brands."""

from .base import BaseScraper


class GrandpaScraper(BaseScraper):
    """Scraper for Grandpa store sale page."""

    def __init__(self):
        super().__init__(
            name="Grandpa",
            sale_url="https://www.grandpa.se/sale",
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


class EtonScraper(BaseScraper):
    """Scraper for ETON Shirts sale page."""

    def __init__(self):
        super().__init__(
            name="ETON",
            sale_url="https://www.etonshirts.com/se/sale",
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


class OscarJacobsonScraper(BaseScraper):
    """Scraper for Oscar Jacobson sale page."""

    def __init__(self):
        super().__init__(
            name="Oscar Jacobson",
            sale_url="https://www.oscarjacobson.com/se/sale",
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


class TigerOfSwedenScraper(BaseScraper):
    """Scraper for Tiger of Sweden sale page."""

    def __init__(self):
        super().__init__(
            name="Tiger of Sweden",
            sale_url="https://www.tigerofsweden.com/se/sale/men/",
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


class RalphLaurenScraper(BaseScraper):
    """Scraper for Ralph Lauren Sweden sale page."""

    def __init__(self):
        super().__init__(
            name="Ralph Lauren",
            sale_url="https://www.ralphlauren.se/en/sale/men",
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
        products = soup.select(".product-card, .product-tile, [data-product-tile]")
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


class BrixtolTextilesScraper(BaseScraper):
    """Scraper for Brixtol Textiles sale page."""

    def __init__(self):
        super().__init__(
            name="Brixtol Textiles",
            sale_url="https://www.brixtoltextiles.com/sale",
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


SWEDISH_MENSWEAR_SCRAPERS = [
    GrandpaScraper,
    EtonScraper,
    OscarJacobsonScraper,
    TigerOfSwedenScraper,
    RalphLaurenScraper,
    BrixtolTextilesScraper,
]
