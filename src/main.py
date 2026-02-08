#!/usr/bin/env python3
"""
Stockholm Fashion Sale Alert System
Main entry point for checking sales and sending notifications.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapers import get_all_scrapers
from src.notifiers import EmailNotifier, NtfyNotifier
from src.utils import SaleState


def check_all_stores(state: SaleState, verbose: bool = False) -> list[dict]:
    """
    Check all stores for sales.

    Args:
        state: SaleState instance to track seen sales
        verbose: Print detailed progress

    Returns:
        List of newly detected sales
    """
    scrapers = get_all_scrapers()
    new_sales = []

    print(f"\n🔍 Checking {len(scrapers)} stores for sales...")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for scraper in scrapers:
        if verbose:
            print(f"   Checking {scraper.name}...", end=" ", flush=True)

        try:
            result = scraper.check()

            if result.get("active", False):
                # Check if this is a new sale
                if state.is_new_sale(scraper.name, result):
                    new_sales.append(result)
                    state.record_sale(scraper.name, result)
                    if verbose:
                        print(f"✅ NEW SALE! {result.get('description', '')}")
                else:
                    if verbose:
                        print(f"📌 Sale ongoing")
                    # Update last seen time
                    state.record_sale(scraper.name, result)
            else:
                # Mark as inactive if was previously active
                if scraper.name in state.state.get("sales", {}):
                    if state.state["sales"][scraper.name].get("active", False):
                        state.mark_inactive(scraper.name)
                        if verbose:
                            print("❌ Sale ended")
                    else:
                        if verbose:
                            print("⬜ No sale")
                else:
                    if verbose:
                        print("⬜ No sale")

        except Exception as e:
            print(f"   ⚠️  {scraper.name}: Error - {e}")

    return new_sales


def send_notifications(new_sales: list[dict]) -> None:
    """Send notifications for new sales via all configured channels."""
    if not new_sales:
        print("\n📭 No new sales to notify about.")
        return

    print(f"\n📬 Sending notifications for {len(new_sales)} new sale(s)...")

    # Email notification
    email_notifier = EmailNotifier()
    if email_notifier.is_configured():
        if email_notifier.send_sale_alert(new_sales):
            print("   ✅ Email sent")
        else:
            print("   ❌ Email failed")
    else:
        print("   ⏭️  Email not configured (skipping)")

    # Phone push notification
    ntfy_notifier = NtfyNotifier()
    if ntfy_notifier.is_configured():
        if ntfy_notifier.send_sale_alert(new_sales):
            print("   ✅ Phone notification sent")
        else:
            print("   ❌ Phone notification failed")
    else:
        print("   ⏭️  Phone (ntfy) not configured (skipping)")


def print_summary(new_sales: list[dict], state: SaleState) -> None:
    """Print a summary of the check."""
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)

    active_sales = state.get_active_sales()
    print(f"\n   New sales found: {len(new_sales)}")
    print(f"   Total active sales: {len(active_sales)}")

    if new_sales:
        print("\n   🆕 NEW SALES:")
        for sale in new_sales:
            print(f"      • {sale['store_name']}: {sale.get('description', 'Sale active')}")
            print(f"        {sale['url']}")

    if active_sales:
        print("\n   📌 ALL ACTIVE SALES:")
        for name, info in active_sales.items():
            print(f"      • {name}: {info.get('description', 'Sale active')}")

    print("\n" + "=" * 50)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Stockholm Fashion Sale Alert System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run full check and notify
  python main.py --verbose          # Run with detailed output
  python main.py --test-notify      # Send a test notification
  python main.py --dry-run          # Check without notifications
  python main.py --store "H&M Men"  # Check a specific store
        """,
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print detailed progress"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Check for sales but don't send notifications",
    )
    parser.add_argument(
        "--test-notify",
        action="store_true",
        help="Send a test notification to verify setup",
    )
    parser.add_argument(
        "--store", "-s", type=str, help="Check a specific store by name"
    )
    parser.add_argument(
        "--state-file",
        type=str,
        default="sale_state.json",
        help="Path to state file (default: sale_state.json)",
    )

    args = parser.parse_args()

    # Test notification mode
    if args.test_notify:
        print("🔔 Sending test notifications...")

        email_notifier = EmailNotifier()
        ntfy_notifier = NtfyNotifier()

        test_sale = [
            {
                "store_name": "Test Store",
                "description": "This is a test notification!",
                "url": "https://example.com",
            }
        ]

        if email_notifier.is_configured():
            email_notifier.send_sale_alert(test_sale)
        else:
            print("   Email not configured")

        if ntfy_notifier.is_configured():
            ntfy_notifier.send_test()
        else:
            print("   ntfy not configured")

        print("\n✅ Test complete!")
        return

    # Initialize state
    state = SaleState(args.state_file)

    # Check specific store or all stores
    if args.store:
        from src.scrapers import get_scraper_by_name

        scraper = get_scraper_by_name(args.store)
        if not scraper:
            print(f"❌ Unknown store: {args.store}")
            print("\nAvailable stores:")
            from src.scrapers import get_all_scrapers

            for s in get_all_scrapers():
                print(f"   • {s.name}")
            sys.exit(1)

        print(f"\n🔍 Checking {scraper.name}...")
        result = scraper.check()
        print(f"\nResult: {result}")
        return

    # Full check
    new_sales = check_all_stores(state, verbose=args.verbose)

    # Send notifications (unless dry run)
    if not args.dry_run:
        send_notifications(new_sales)

    # Print summary
    print_summary(new_sales, state)

    # Save state
    state.save()
    print(f"\n💾 State saved to {args.state_file}")


if __name__ == "__main__":
    main()
