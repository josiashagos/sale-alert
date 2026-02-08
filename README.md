# Stockholm Fashion Sale Alert System

A cloud-hosted system that monitors Swedish and international fashion retailers for sales, sending you email and phone notifications when sales start.

## Features

- **27 Fashion Retailers**: Tracks H&M Group, Zara, Mango, Acne Studios, Our Legacy, SSENSE, Mr Porter, and more
- **Automatic Checks**: Runs twice daily via GitHub Actions (8 AM and 6 PM Stockholm time)
- **Smart Notifications**: Only alerts you when NEW sales start (no spam)
- **Multiple Channels**: Email + Phone push notifications (via ntfy.sh)
- **Free**: No hosting costs - runs on GitHub Actions free tier

## Quick Start

### 1. Fork This Repository

Click the "Fork" button at the top of this repository.

### 2. Set Up Phone Notifications (ntfy.sh)

1. Download the **ntfy** app on your phone:
   - [iPhone App Store](https://apps.apple.com/app/ntfy/id1625396347)
   - [Android Play Store](https://play.google.com/store/apps/details?id=io.heckel.ntfy)

2. Open the app, tap the + button, and subscribe to a **unique private topic** like:
   ```
   stockholm-sales-yourname-xyz123
   ```
   (Add random characters so no one else can guess it)

3. Test it works by visiting `https://ntfy.sh/YOUR-TOPIC-NAME` in a browser and sending a message

### 3. Set Up Email Notifications

1. In your Gmail account:
   - Go to Settings → Security → 2-Step Verification
   - Scroll down to "App passwords" and generate one for "Mail"

2. Note: If you don't want email notifications, you can skip this step

### 4. Add GitHub Secrets

In your forked repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `NTFY_TOPIC` | Your ntfy topic (e.g., `stockholm-sales-yourname-xyz123`) |
| `EMAIL_ADDRESS` | Your Gmail address (optional) |
| `EMAIL_APP_PASSWORD` | Your Gmail app password (optional) |

### 5. Enable GitHub Actions

1. Go to the **Actions** tab in your forked repository
2. Click "I understand my workflows, go ahead and enable them"
3. Done! The system will run automatically at 8 AM and 6 PM Stockholm time

### 6. Test It

1. Go to **Actions** → **Check Fashion Sales**
2. Click **Run workflow** → **Run workflow**
3. Check your phone for a notification (if any sales are active)

## What You'll Receive

When a new sale is detected, you'll get a notification like:

```
🛍️ Sale at H&M Men
Up to 50% off
[Tap to open sale page]
```

## Tracked Stores

### Swedish Mass Market (H&M Group)
- H&M Men, COS Men, Arket Men, Weekday Men

### International Fast Fashion
- Zara Man, Mango Man, Uniqlo Men, Massimo Dutti Men

### Scandinavian Brands
- Our Legacy, Samsøe Samsøe, Acne Studios, Norse Projects, NN07

### Premium/Designer
- END. Clothing, Louis Vuitton, Mr Porter, SSENSE, Matches

### Online-First Swedish
- Boozt Men, Zalando Men, Caliroots, Tres Bien

### Department Stores
- NK Herr, Åhléns Herr

### Streetwear/Sneakers
- Sneakersnstuff, Footish, Solebox

## Customization

### Disable a Store

Edit `stores.json` and set `"enabled": false` for any store:

```json
{
  "name": "Louis Vuitton",
  "enabled": false
}
```

### Change Check Frequency

Edit `.github/workflows/check-sales.yml`:

```yaml
schedule:
  - cron: '0 7 * * *'   # 8:00 AM CET
  - cron: '0 12 * * *'  # Add more times as needed
  - cron: '0 17 * * *'  # 6:00 PM CET
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run a check
python src/main.py --verbose

# Test notifications
python src/main.py --test-notify

# Check specific store
python src/main.py --store "H&M Men"

# Dry run (no notifications)
python src/main.py --dry-run
```

## Troubleshooting

### "No new sales" but stores have sales?

The system only notifies for **new** sales. If a sale was already running when you set up the system, it won't alert you. To reset:

1. Delete `sale_state.json`
2. Run the check again

### Not receiving phone notifications?

1. Make sure you subscribed to the exact topic name in the ntfy app
2. Check the app has notification permissions on your phone
3. Test by visiting `https://ntfy.sh/YOUR-TOPIC` and sending a message

### GitHub Actions not running?

1. Make sure Actions are enabled in your forked repository
2. Check the Actions tab for any error messages
3. Try running manually with "Run workflow"

## Cost

**$0/month** - Everything runs on free tiers:
- GitHub Actions: Free for public repositories
- Gmail SMTP: Free (500 emails/day)
- ntfy.sh: Free (unlimited push notifications)

## Contributing

Feel free to add more stores! Create a new scraper in `src/scrapers/` following the existing pattern.

## License

MIT
