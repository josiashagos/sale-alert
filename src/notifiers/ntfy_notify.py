"""Phone push notifications via ntfy.sh."""

import json
import os
from typing import Optional

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
        Send a push notification using JSON API (supports UTF-8).
        """
        if not self.is_configured():
            print("ntfy not configured - skipping phone notification")
            return False

        try:
            payload = {
                "topic": self.topic,
                "title": title,
                "message": message,
                "priority": 4 if priority == "high" else 3,
            }

            if tags:
                payload["tags"] = tags

            if click_url:
                payload["click"] = click_url

            response = requests.post(
                self.base_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()

            print(f"Phone notification sent to topic: {self.topic}")
            return True

        except Exception as e:
            print(f"Failed to send phone notification: {e}")
            return False

    def send_sale_alert(self, new_sales: list[dict]) -> bool:
        """Send a formatted sale alert notification."""
        if not new_sales:
            return False

        if len(new_sales) == 1:
            sale = new_sales[0]
            title = f"REA: {sale['store_name']}"
            message = sale.get("description", "REA pågår!")
            click_url = sale["url"]
        else:
            title = f"{len(new_sales)} nya reor!"
            store_names = [s["store_name"] for s in new_sales[:5]]
            if len(new_sales) > 5:
                store_names.append(f"+{len(new_sales) - 5} till")
            message = ", ".join(store_names)
            click_url = new_sales[0]["url"]

        return self.send(
            title=title,
            message=message,
            priority="high",
            tags=["shopping_bags"],
            click_url=click_url,
        )

    def send_test(self) -> bool:
        """Send a test notification to verify setup."""
        return self.send(
            title="Test",
            message="Stockholm Fashion Sale Alert fungerar!",
            priority="default",
            tags=["white_check_mark"],
        )
