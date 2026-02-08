"""Base scraper class with common functionality."""

import re
import time
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """Base class for all store scrapers."""

    # Common sale-related keywords across languages
    SALE_KEYWORDS = [
        # Swedish
        "rea",
        "rabatt",
        "erbjudande",
        "kampanj",
        "prisnedsättning",
        "slutrea",
        "mellanrea",
        # English
        "sale",
        "discount",
        "off",
        "clearance",
        "outlet",
        "reduced",
        "markdown",
        "promo",
        "deal",
        # Percentage patterns
        r"\d+\s*%",
    ]

    def __init__(
        self,
        name: str,
        sale_url: str,
        keywords: Optional[list[str]] = None,
        use_playwright: bool = False,
    ):
        self.name = name
        self.sale_url = sale_url
        self.keywords = keywords or self.SALE_KEYWORDS
        self.use_playwright = use_playwright
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8",
            }
        )

    def fetch_page(self, url: Optional[str] = None) -> Optional[str]:
        """
        Fetch page content using requests or playwright.

        Args:
            url: URL to fetch, defaults to sale_url

        Returns:
            Page HTML content or None if failed
        """
        target_url = url or self.sale_url

        if self.use_playwright:
            return self._fetch_with_playwright(target_url)
        return self._fetch_with_requests(target_url)

    def _fetch_with_requests(self, url: str) -> Optional[str]:
        """Fetch page using requests library."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[{self.name}] Request failed: {e}")
            return None

    def _fetch_with_playwright(self, url: str) -> Optional[str]:
        """Fetch page using playwright for JavaScript-heavy sites."""
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
                page.goto(url, wait_until="networkidle", timeout=60000)
                # Wait a bit for dynamic content
                time.sleep(2)
                content = page.content()
                browser.close()
                return content
        except Exception as e:
            print(f"[{self.name}] Playwright fetch failed: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content into BeautifulSoup object."""
        return BeautifulSoup(html, "lxml")

    def has_sale_indicators(self, soup: BeautifulSoup) -> tuple[bool, str]:
        """
        Check if page contains sale indicators.

        Returns:
            Tuple of (has_sale, description)
        """
        text_content = soup.get_text().lower()

        # Check for keywords
        found_keywords = []
        for keyword in self.keywords:
            if keyword.startswith(r"\\"):
                # Regex pattern
                if re.search(keyword, text_content, re.IGNORECASE):
                    found_keywords.append("discount percentage")
            elif keyword.lower() in text_content:
                found_keywords.append(keyword)

        if found_keywords:
            # Try to extract discount percentage
            percentage = self._extract_max_discount(text_content)
            if percentage:
                description = f"Up to {percentage}% off"
            else:
                description = f"Sale active ({', '.join(found_keywords[:3])})"
            return True, description

        return False, ""

    def _extract_max_discount(self, text: str) -> Optional[int]:
        """Extract the maximum discount percentage from text."""
        # Common patterns: "up to 50%", "50% off", "-50%", "50 %"
        patterns = [
            r"(?:up to|upp till|bis zu)\s*(\d+)\s*%",
            r"(\d+)\s*%\s*(?:off|rabatt|av)",
            r"-\s*(\d+)\s*%",
            r"(\d+)\s*%",
        ]

        max_discount = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    discount = int(match)
                    if 5 <= discount <= 90:  # Reasonable discount range
                        max_discount = max(max_discount, discount)
                except ValueError:
                    continue

        return max_discount if max_discount > 0 else None

    def count_sale_items(self, soup: BeautifulSoup) -> int:
        """
        Try to count the number of sale items.
        Override in subclass for store-specific logic.
        """
        # Generic approach: count product cards
        selectors = [
            ".product-card",
            ".product-item",
            ".product",
            '[data-testid="product"]',
            ".item",
        ]

        for selector in selectors:
            items = soup.select(selector)
            if items:
                return len(items)

        return 0

    @abstractmethod
    def check_sale(self) -> dict:
        """
        Check if there's an active sale.

        Returns:
            Dictionary with:
            - active: bool
            - description: str
            - url: str
            - store_name: str
            - item_count: int (optional)
        """
        pass

    def check(self) -> dict:
        """Main entry point to check for sales."""
        try:
            return self.check_sale()
        except Exception as e:
            print(f"[{self.name}] Error checking sale: {e}")
            return {
                "active": False,
                "store_name": self.name,
                "url": self.sale_url,
                "error": str(e),
            }
