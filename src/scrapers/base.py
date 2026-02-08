"""Base scraper class with common functionality."""

import re
import time
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class BaseScraper:
    """Base class for all store scrapers."""

    # Strong sale keywords - these indicate a sale is happening
    SALE_KEYWORDS_STRONG = [
        r"\brea\b",
        r"\bsale\b",
        r"\bslutrea\b",
        r"\bmellanrea\b",
        r"\bvinterrea\b",
        r"\bsommarrea\b",
        r"\bclearance\b",
        r"\boutlet\b",
    ]

    # Discount patterns
    DISCOUNT_PATTERNS = [
        r"(\d{1,2})\s*%\s*(?:rabatt|off|av)",
        r"(?:up to|upp till|spara)\s*(\d{1,2})\s*%",
        r"-\s*(\d{1,2})\s*%",
    ]

    def __init__(
        self,
        name: str,
        base_url: str,
        sale_path: Optional[str] = None,
        use_playwright: bool = True,
    ):
        """
        Initialize scraper.

        Args:
            name: Store name
            base_url: Main page URL (e.g., men's section)
            sale_path: Optional path to dedicated sale page
            use_playwright: Use browser for JS-heavy sites
        """
        self.name = name
        self.base_url = base_url
        self.sale_path = sale_path
        self.use_playwright = use_playwright
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8",
        })

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content."""
        if self.use_playwright:
            return self._fetch_with_playwright(url)
        return self._fetch_with_requests(url)

    def _fetch_with_requests(self, url: str) -> Optional[str]:
        """Fetch page using requests."""
        try:
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[{self.name}] Request failed: {e}")
            return None

    def _fetch_with_playwright(self, url: str) -> Optional[str]:
        """Fetch page using playwright for JS-heavy sites."""
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    locale="sv-SE",
                )
                page = context.new_page()

                # Block heavy resources to speed up
                page.route("**/*.{png,jpg,jpeg,gif,webp,svg}", lambda route: route.abort())

                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                time.sleep(2)  # Wait for dynamic content
                content = page.content()
                browser.close()
                return content
        except Exception as e:
            print(f"[{self.name}] Playwright fetch failed: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content."""
        return BeautifulSoup(html, "lxml")

    def detect_sale(self, soup: BeautifulSoup) -> tuple[bool, str, Optional[str]]:
        """
        Detect if there's a sale on the page.

        Looks for:
        - Sale keywords in headers, banners, navigation
        - Discount percentages
        - Links to sale pages

        Returns:
            (has_sale, description, sale_link)
        """
        # Areas where sales are typically announced
        important_selectors = [
            "header", "nav", ".banner", ".hero",
            ".announcement", ".promo", ".campaign",
            "[class*='sale']", "[class*='rea']",
            "[class*='banner']", "[class*='offer']",
            "h1", "h2", "h3", "a"
        ]

        important_text = ""
        for selector in important_selectors:
            for el in soup.select(selector):
                important_text += " " + el.get_text()

        important_text = important_text.lower()
        full_text = soup.get_text().lower()

        # Check for strong sale keywords
        for pattern in self.SALE_KEYWORDS_STRONG:
            if re.search(pattern, important_text, re.IGNORECASE):
                discount = self._extract_discount(important_text) or self._extract_discount(full_text)
                description = f"Upp till {discount}% rabatt" if discount else "REA pågår"
                sale_link = self._find_sale_link(soup)
                return True, description, sale_link

        # Check for discount percentages
        for pattern in self.DISCOUNT_PATTERNS:
            match = re.search(pattern, important_text, re.IGNORECASE)
            if match:
                try:
                    discount = int(match.group(1))
                    if 10 <= discount <= 80:
                        description = f"Upp till {discount}% rabatt"
                        sale_link = self._find_sale_link(soup)
                        return True, description, sale_link
                except (ValueError, IndexError):
                    pass

        return False, "", None

    def _extract_discount(self, text: str) -> Optional[int]:
        """Extract max discount percentage from text."""
        matches = re.findall(r"(\d{1,2})\s*%", text)
        valid_discounts = []
        for m in matches:
            try:
                d = int(m)
                if 10 <= d <= 80:
                    valid_discounts.append(d)
            except ValueError:
                pass
        return max(valid_discounts) if valid_discounts else None

    def _find_sale_link(self, soup: BeautifulSoup) -> Optional[str]:
        """Find a link to the sale page."""
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            link_text = link.get_text().lower()

            # Check link text for sale words
            if any(w in link_text for w in ["sale", "rea", "rabatt", "erbjudande", "kampanj"]):
                return self._normalize_url(href)

            # Check URL for sale paths
            if re.search(r"/(sale|rea|outlet|kampanj|erbjudande)", href, re.IGNORECASE):
                return self._normalize_url(href)

        return None

    def _normalize_url(self, href: str) -> str:
        """Convert relative URL to absolute."""
        if href.startswith("http"):
            return href
        return urljoin(self.base_url, href)

    def check_sale(self) -> dict:
        """
        Check if there's an active sale.

        Returns dict with: active, store_name, url, description
        """
        # Check main page for sale announcements
        html = self.fetch_page(self.base_url)
        if not html:
            return {
                "active": False,
                "store_name": self.name,
                "url": self.base_url,
                "error": "Failed to fetch page",
            }

        soup = self.parse_html(html)
        has_sale, description, sale_link = self.detect_sale(soup)

        if has_sale:
            return {
                "active": True,
                "store_name": self.name,
                "url": sale_link or self.base_url,
                "description": description,
            }

        # If no sale found on main page, check dedicated sale page if exists
        if self.sale_path:
            sale_url = self._normalize_url(self.sale_path)
            html = self.fetch_page(sale_url)
            if html:
                soup = self.parse_html(html)
                # Check if sale page has products (indicates active sale)
                products = soup.select(".product, .product-card, .product-item, [data-product]")
                if len(products) > 5:  # More than 5 products = active sale
                    discount = self._extract_discount(soup.get_text().lower())
                    description = f"Upp till {discount}% rabatt" if discount else "REA pågår"
                    return {
                        "active": True,
                        "store_name": self.name,
                        "url": sale_url,
                        "description": description,
                    }

        return {
            "active": False,
            "store_name": self.name,
            "url": self.base_url,
        }

    def check(self) -> dict:
        """Main entry point."""
        try:
            return self.check_sale()
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            return {
                "active": False,
                "store_name": self.name,
                "url": self.base_url,
                "error": str(e),
            }
