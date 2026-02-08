"""Email notification sender using Gmail SMTP."""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional


class EmailNotifier:
    """Send email notifications for new sales."""

    def __init__(
        self,
        email_address: Optional[str] = None,
        app_password: Optional[str] = None,
    ):
        self.email_address = email_address or os.getenv("EMAIL_ADDRESS")
        self.app_password = app_password or os.getenv("EMAIL_APP_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def is_configured(self) -> bool:
        """Check if email notifications are properly configured."""
        return bool(self.email_address and self.app_password)

    def send(self, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send an email notification.

        Args:
            subject: Email subject line
            body: Plain text body
            html_body: Optional HTML body for rich formatting

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_configured():
            print("Email not configured - skipping email notification")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.email_address
            msg["To"] = self.email_address

            # Add plain text part
            msg.attach(MIMEText(body, "plain", "utf-8"))

            # Add HTML part if provided
            if html_body:
                msg.attach(MIMEText(html_body, "html", "utf-8"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.app_password)
                server.send_message(msg)

            print(f"Email sent successfully to {self.email_address}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_sale_alert(self, new_sales: list[dict]) -> bool:
        """
        Send a formatted sale alert email.

        Args:
            new_sales: List of sale dictionaries with store info

        Returns:
            True if sent successfully
        """
        if not new_sales:
            return False

        subject = f"🛍️ {len(new_sales)} New Sale{'s' if len(new_sales) > 1 else ''} Detected!"

        # Plain text body
        body_lines = ["NEW SALES DETECTED\n", "=" * 40, ""]
        for sale in new_sales:
            body_lines.extend(
                [
                    f"📍 {sale['store_name']}",
                    f"   {sale.get('description', 'Sale active')}",
                    f"   Link: {sale['url']}",
                    "",
                ]
            )
        body_lines.append("\nHappy shopping! 🎉")
        body = "\n".join(body_lines)

        # HTML body
        html_items = ""
        for sale in new_sales:
            html_items += f"""
            <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff;">
                <h3 style="margin: 0 0 8px 0; color: #333;">{sale['store_name']}</h3>
                <p style="margin: 0 0 8px 0; color: #666;">{sale.get('description', 'Sale active')}</p>
                <a href="{sale['url']}" style="color: #007bff; text-decoration: none;">Shop Now →</a>
            </div>
            """

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #333;">🛍️ New Sales Detected!</h1>
            <p style="color: #666;">The following stores have started new sales:</p>
            {html_items}
            <p style="color: #999; font-size: 12px; margin-top: 30px;">
                Sent by Stockholm Fashion Sale Alert
            </p>
        </body>
        </html>
        """

        return self.send(subject, body, html_body)
