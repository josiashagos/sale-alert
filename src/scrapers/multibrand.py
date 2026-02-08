"""Scrapers for multi-brand retailers."""

from .base import BaseScraper


class CareOfCarlScraper(BaseScraper):
    """Scraper for Care of Carl sale page - multi-brand menswear retailer."""

    def __init__(self):
        super().__init__(
            name="Care of Carl",
            sale_url="https://www.careofcarl.se/sv/sale/",
            keywords=["sale", "rea", "% rabatt", "rabatt"],
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
                "description": description or "REA active (Oscar Jacobson, ETON, Tiger, etc.)",
                "item_count": len(products),
            }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.sale_url,
        }


MULTIBRAND_SCRAPERS = [CareOfCarlScraper]
