"""State management for tracking seen sales."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class SaleState:
    """Manages the state of detected sales to prevent duplicate notifications."""

    def __init__(self, state_file: str = "sale_state.json"):
        self.state_file = Path(state_file)
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """Load state from file or create new state."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"sales": {}, "last_check": None}

    def save(self) -> None:
        """Save current state to file."""
        self.state["last_check"] = datetime.now().isoformat()
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def is_new_sale(self, store_name: str, sale_info: dict) -> bool:
        """
        Check if this is a new sale we haven't seen before.

        A sale is considered "new" if:
        - We've never seen a sale from this store
        - The sale details have changed significantly
        """
        if store_name not in self.state["sales"]:
            return True

        existing = self.state["sales"][store_name]

        # If the sale was previously marked as inactive and is now active
        if not existing.get("active", False) and sale_info.get("active", False):
            return True

        return False

    def record_sale(self, store_name: str, sale_info: dict) -> None:
        """Record a sale in the state."""
        self.state["sales"][store_name] = {
            **sale_info,
            "first_seen": self.state["sales"].get(store_name, {}).get(
                "first_seen", datetime.now().isoformat()
            ),
            "last_seen": datetime.now().isoformat(),
        }

    def mark_inactive(self, store_name: str) -> None:
        """Mark a store's sale as inactive (sale has ended)."""
        if store_name in self.state["sales"]:
            self.state["sales"][store_name]["active"] = False
            self.state["sales"][store_name]["ended"] = datetime.now().isoformat()

    def get_active_sales(self) -> dict:
        """Get all currently active sales."""
        return {
            name: info
            for name, info in self.state["sales"].items()
            if info.get("active", False)
        }

    def get_last_check(self) -> Optional[str]:
        """Get the timestamp of the last check."""
        return self.state.get("last_check")
