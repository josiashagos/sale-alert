"""Scrapers for H&M Group stores (H&M, COS, Arket, Weekday)."""

from typing import Optional

from .base import BaseScraper


class HMScraper(BaseScraper):
    """Scraper for H&M Men's sale page."""

    def __init__(self):
        super().__init__(
            name="H&M Men",
            sale_url="https://www2.hm.com/sv_se/herr/kampanjer-erbjudanden/rea.html",
            keywords=["rea", "rabatt", "% rabatt", "erbjudande"],
            use_playwright=True,  # H&M uses heavy JavaScript
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

        # H&M specific: Check for product listings on sale page
        # If the page has products, sale is active
        products = soup.select(".product-item, .hm-product-item, [data-productid]")
        has_products = len(products) > 0

        # Also check for sale text
        has_sale, description = self.has_sale_indicators(soup)

        if has_products or has_sale:
            item_count = len(products) if products else self.count_sale_items(soup)
            return {
                "active": True,
                "store_name": self.name,
                "url": self.sale_url,
                "description": description or f"REA - {item_count}+ items",
                "item_count": item_count,
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


class COSScraper(BaseScraper):
    """Scraper for COS Men's sale page."""

    def __init__(self):
        super().__init__(
            name="COS Men",
            sale_url="https://www.cos.com/sv-se/men/sale.html",
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

        # Check for product grid
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


class ArketScraper(BaseScraper):
    """Scraper for Arket Men's sale page."""

    def __init__(self):
        super().__init__(
            name="Arket Men",
            sale_url="https://www.arket.com/sv-se/men/sale.html",
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
        products = soup.select(".product-card, .product-item, [data-product]")
        has_sale, description = self.has_sale_indicators(soup)

        if len(products) > 0 or has_sale:
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


class WeekdayScraper(BaseScraper):
    """Scraper for Weekday Men's sale page."""

    def __init__(self):
        super().__init__(
            name="Weekday Men",
            sale_url="https://www.weekday.com/sv-se/men/sale.html",
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
        products = soup.select(".product-card, .product-item, [data-product]")
        has_sale, description = self.has_sale_indicators(soup)

        if len(products) > 0 or has_sale:
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


# Export all scrapers
HM_GROUP_SCRAPERS = [HMScraper, COSScraper, ArketScraper, WeekdayScraper]
