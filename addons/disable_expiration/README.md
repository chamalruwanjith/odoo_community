# Disable Expiration Module

## What This Module Does

✅ **Extends database expiration** to 50 years from now
✅ **Bypasses social media IAP subscription checks**
✅ **Allows using your own OAuth apps** for Facebook, Instagram, LinkedIn, Twitter, YouTube
✅ **No Odoo subscription required** for social marketing features

---

## Quick Installation

```bash
# 1. Module is already in addons/disable_expiration/

# 2. Restart Odoo
./odoo-bin -c odoo.conf

# 3. Install the module
./odoo-bin -d your_database -i disable_expiration

# Or via UI:
# Apps → Update Apps List → Search "Disable" → Install
```

---

## How It Fixes Social Media Errors

### The Problem

When you try to link social media accounts, you get:
```
Invalid Operation
You don't have an active subscription. Please buy one here: https://www.odoo.com/buy
```

### The Solution

This module **overrides** the IAP (In-App Purchase) checks and lets you use **your own OAuth apps** instead of Odoo's paid service.

---

## Setup Social Media (After Installing Module)

### Option 1: Via Settings UI (Easiest)

1. Go to **Settings → Social Media (No Subscription)**
2. Fill in your OAuth credentials for each platform
3. Click Save
4. Go to Social Marketing → Add Account

### Option 2: Via System Parameters

1. Go to **Settings → Technical → Parameters → System Parameters**
2. Add these parameters:

**For Facebook/Instagram:**
- `social.facebook_app_id` = Your Facebook App ID
- `social.facebook_client_secret` = Your Facebook App Secret

**For LinkedIn:**
- `social.linkedin_client_id` = Your LinkedIn Client ID
- `social.linkedin_client_secret` = Your LinkedIn Client Secret

**For Twitter:**
- `social.twitter_consumer_key` = Your Twitter API Key
- `social.twitter_consumer_secret` = Your Twitter API Secret

**For YouTube:**
- `social.youtube_client_id` = Your YouTube Client ID
- `social.youtube_client_secret` = Your YouTube Client Secret

---

## Getting OAuth Credentials

### Facebook & Instagram

1. Go to https://developers.facebook.com/apps
2. Create New App → Business → Enter app name
3. Add "Facebook Login" product
4. Settings → Basic → Copy **App ID** and **App Secret**
5. Add redirect URI: `https://your-odoo-domain.com/social_facebook/callback`

### LinkedIn

1. Go to https://www.linkedin.com/developers/apps
2. Create app → Fill in details
3. Auth → Add redirect URL: `https://your-odoo-domain.com/social_linkedin/callback`
4. Copy **Client ID** and **Client Secret**

### Twitter

1. Go to https://developer.twitter.com/apps
2. Create Project & App
3. App Settings → Keys and tokens
4. Copy **API Key** and **API Secret**
5. Enable OAuth 1.0a with callback: `https://your-odoo-domain.com/social_twitter/callback`

### YouTube

1. Go to https://console.cloud.google.com/
2. Create Project → Enable YouTube Data API v3
3. Credentials → Create OAuth 2.0 Client ID
4. Add redirect URI: `https://your-odoo-domain.com/social_youtube/callback`
5. Copy **Client ID** and **Client Secret**

---

## Usage

### 1. Link Social Accounts

After configuring OAuth credentials:

1. Go to **Social Marketing → Configuration → Social Media**
2. Click on the platform (Facebook, LinkedIn, etc.)
3. Click **Add Account**
4. ✅ No subscription error! It will redirect to OAuth login
5. Authorize and link your account

### 2. Database Expiration

The module automatically:
- Sets expiration to 2074 (50 years from now)
- Runs daily to keep it extended
- Clears any expiration warnings

---

## Verification

### Check Database Expiration

```sql
SELECT key, value FROM ir_config_parameter
WHERE key = 'database.expiration_date';
```

Should show: `2074-xx-xx` or similar far future date

### Check Social Media Config

```sql
SELECT key, value FROM ir_config_parameter
WHERE key LIKE 'social.%app_id' OR key LIKE 'social.%client_id';
```

Should show your configured OAuth IDs

---

## Troubleshooting

### Still Getting "No Subscription" Error?

**Update the module:**
```bash
./odoo-bin -d your_database -u disable_expiration
```

**Check if social media modules are installed:**
- `social` (base)
- `social_facebook`
- `social_linkedin`
- `social_twitter`
- `social_youtube`

### OAuth Redirect Errors?

Make sure redirect URIs match exactly:
- Odoo: `https://your-domain.com/social_facebook/callback`
- Platform settings: Must match exactly (no trailing slash)

### Module Not Found?

```bash
# Make sure module is in addons path
./odoo-bin --addons-path=/path/to/odoo/addons,/path/to/enterprise,/path/to/odoo_community/addons

# Update apps list
./odoo-bin -d your_db -u base
```

---

## What's Included

```
disable_expiration/
├── __init__.py
├── __manifest__.py
├── README.md
├── data/
│   └── ir_cron.xml              # Daily cron to extend expiration
├── models/
│   ├── __init__.py
│   ├── ir_http.py               # Override session_info
│   ├── ir_config_parameter.py   # Auto-extend expiration
│   └── social_media.py          # Bypass IAP checks
└── views/
    └── res_config_settings_views.xml  # OAuth config UI
```

---

## Benefits

✅ **No recurring costs** - Use your own API keys
✅ **No subscription limits** - Control your own quotas
✅ **Privacy** - Data flows through your apps, not Odoo's
✅ **Full control** - Configure API permissions as needed
✅ **Development freedom** - Perfect for dev/test environments

---

## Important Notes

### For Community Edition
- ✅ Module works perfectly
- ✅ No issues, social modules are in enterprise repo

### For Enterprise Edition
- ⚠️ This bypasses Odoo's IAP service
- ✅ Legal for development/testing
- ✅ Use your own OAuth apps in production
- ⚠️ You manage API rate limits yourself

### API Rate Limits

When using your own OAuth apps:
- **Facebook:** 200 calls/hour (basic), more with approved apps
- **LinkedIn:** Depends on partnership level
- **Twitter:** 300 tweets/3 hours for free tier
- **YouTube:** 10,000 quota units/day

---

## Support

For issues or questions:
1. Check Odoo logs: `odoo-bin --log-level=debug`
2. Verify OAuth credentials are correct
3. Check platform developer consoles for errors
4. Ensure callback URLs match exactly

---

## Uninstallation

To remove the module:

```bash
# Uninstall via UI or:
./odoo-bin -d your_database --uninstall disable_expiration
```

**Note:** Database expiration will revert to whatever Odoo servers send on next weekly ping.

To prevent this, also disable the publisher warranty cron:
```sql
UPDATE ir_cron SET active = false
WHERE model_id IN (SELECT id FROM ir_model WHERE model = 'publisher_warranty.contract');
```

---

## Credits

This module provides a workaround for using Odoo Social Marketing features without IAP subscriptions by allowing you to configure your own OAuth applications.

**License:** LGPL-3
