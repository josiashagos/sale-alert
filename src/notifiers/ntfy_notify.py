"""Phone push notifications via ntfy.sh."""

import os
from typing import Optional
from urllib.parse import quote

import requests


class NtfyNotifier:
    """Send push notifications to phone via ntfy.sh."""

    def __init__(self, topic: Optional[str] = None):
        self.topic = topic or os.getenv("NTFY_TOPIC")
        self.base_url = "https://ntfy.sh"

    def is_configured(self) -> bool:
        """Check if ntfy notifications are properly configured."""
        return bool(self.topic)

    def send(
        self,
        title: str,
        message: str,
        priority: str = "default",
        tags: Optional[list[str]] = None,
        click_url: Optional[str] = None,
    ) -> bool:
        """
        Send a push notification.

        Args:
            title: Notification title
            message: Notification body
            priority: Priority level (min, low, default, high, urgent)
            tags: List of emoji tags (e.g., ["shopping_bags", "tada"])
            click_url: URL to open when notification is tapped

        Returns:
            True if sent successfully
        """
        if not self.is_configured():
            print("ntfy not configured - skipping phone notification")
            return False

        try:
            headers = {
                "Title": title,
                "Priority": priority,
            }

            if tags:
                headers["Tags"] = ",".join(tags)

            if click_url:
                headers["Click"] = click_url

            response = requests.post(
                f"{self.base_url}/{self.topic}",
                data=message.encode("utf-8"),
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()

            print(f"Phone notification sent to topic: {self.topic}")
            return True

        except Exception as e:
            print(f"Failed to send phone notification: {e}")
            return False

    def send_sale_alert(self, new_sales: list[dict]) -> bool:
        """
        Send a formatted sale alert notification.

        Args:
            new_sales: List of sale dictionaries with store info

        Returns:
            True if sent successfully
        """
        if not new_sales:
            return False

        if len(new_sales) == 1:
            sale = new_sales[0]
            title = f"🛍️ Sale at {sale['store_name']}"
            message = sale.get("description", "Sale is now active!")
            click_url = sale["url"]
        else:
            title = f"🛍️ {len(new_sales)} New Sales!"
            store_names = [s["store_name"] for s in new_sales[:5]]
            if len(new_sales) > 5:
                store_names.append(f"+{len(new_sales) - 5} more")
            message = ", ".join(store_names)
            # Link to first sale
            click_url = new_sales[0]["url"]

        return self.send(
            title=title,
            message=message,
            priority="high",
            tags=["shopping_bags", "moneybag"],
            click_url=click_url,
        )

    def send_test(self) -> bool:
        """Send a test notification to verify setup."""
        return self.send(
            title="🔔 Test Notification",
            message="Stockholm Fashion Sale Alert is working!",
            priority="default",
            tags=["white_check_mark"],
        )
