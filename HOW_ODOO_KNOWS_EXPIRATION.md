# How Odoo Knows When Database Expires - Complete Flow

## TL;DR
**Yes, Odoo pings external servers!** It's not just about local subscription management - your Odoo database actively communicates with Odoo's servers weekly to check expiration status.

---

## The Complete Expiration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     YOUR ODOO DATABASE                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Every Week (Cron Job)
                              ▼
        ┌──────────────────────────────────────────┐
        │  publisher_warranty.contract Model       │
        │  (addons/mail/models/update.py)          │
        └──────────────────────────────────────────┘
                              │
                              │ SENDS to Odoo Servers:
                              │ ┌─────────────────────────┐
                              │ │ - database.uuid         │
                              │ │ - database.create_date  │
                              │ │ - enterprise_code       │
                              │ │ - nbr_users (count)     │
                              │ │ - installed apps list   │
                              │ │ - company info          │
                              │ └─────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│            http://services.odoo.com/publisher-warranty/          │
│                      ODOO LICENSE SERVER                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ VALIDATES & RESPONDS:
                              │ ┌─────────────────────────┐
                              │ │ enterprise_info {       │
                              │ │   expiration_date       │
                              │ │   expiration_reason     │
                              │ │   enterprise_code       │
                              │ │   messages/warnings     │
                              │ │ }                       │
                              │ └─────────────────────────┘
                              ▼
        ┌──────────────────────────────────────────┐
        │  ir.config_parameter (Database)          │
        │  UPDATES:                                │
        │  - database.expiration_date              │
        │  - database.expiration_reason            │
        │  - database.enterprise_code              │
        └──────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────────┐
        │  web_enterprise Module (if installed)    │
        │  - Reads expiration_date                 │
        │  - Shows warnings if < 30 days           │
        │  - Blocks access if expired              │
        └──────────────────────────────────────────┘
```

---

## The Automatic Ping System

### 1. **Scheduled Cron Job** (`addons/mail/data/ir_cron_data.xml:15-25`)

```xml
<record id="ir_cron_module_update_notification" model="ir.cron">
    <field name="name">Publisher: Update Notification</field>
    <field name="model_id" ref="model_publisher_warranty_contract"/>
    <field name="code">model.update_notification(None)</field>
    <field name="interval_type">weeks</field>
    <field name="interval_number">1</field>
</record>
```

**Runs**: Every 1 week
**What it does**: Calls `update_notification()` method

---

### 2. **Data Collection** (`addons/mail/models/update.py:23-61`)

Your database collects and sends:

```python
msg = {
    "dbuuid": "abc-123-def...",           # Unique database identifier
    "nbr_users": 15,                      # Total users
    "nbr_active_users": 8,                # Active users (last 15 days)
    "dbname": "your_database",
    "db_create_date": "2024-01-01",
    "version": "18.0",
    "enterprise_code": "ENT-12345",       # Your license code (if exists)
    "apps": ["sale", "purchase", ...],    # All installed apps
    "web_base_url": "https://yoursite.com",
    "company": {...}                      # Company name, email, phone
}
```

---

### 3. **Server Communication** (`addons/mail/models/update.py:71-75`)

```python
url = config.get("publisher_warranty_url")
# Default: http://services.odoo.com/publisher-warranty/

r = requests.post(url, data={'arg0': str(msg), 'action': 'update'}, timeout=30)
result = literal_eval(r.text)
```

**Target Server**: `http://services.odoo.com/publisher-warranty/`

---

### 4. **Server Response Processing** (`addons/mail/models/update.py:101-109`)

Odoo servers respond with:

```python
{
    "messages": ["Your subscription expires in 25 days..."],
    "enterprise_info": {
        "expiration_date": "2024-12-31",
        "expiration_reason": "trial",  # or "subscription", or empty
        "enterprise_code": "ENT-12345",
        "database_already_linked_subscription_url": "...",
        "database_already_linked_email": "..."
    }
}
```

Then Odoo **automatically updates** your database:

```python
if result.get('enterprise_info'):
    set_param = self.env['ir.config_parameter'].sudo().set_param
    set_param('database.expiration_date', result['enterprise_info'].get('expiration_date'))
    set_param('database.expiration_reason', result['enterprise_info'].get('expiration_reason', 'trial'))
    set_param('database.enterprise_code', result['enterprise_info'].get('enterprise_code'))
```

---

## What Odoo Servers Check

The Odoo license server validates:

1. **Enterprise Code**: Is it valid? Is it already used elsewhere?
2. **User Count**: Does it match your subscription tier?
3. **Subscription Status**: Active, expired, trial?
4. **Database UUID**: First-time registration or existing database?

Based on this, it responds with:
- ✅ **Valid subscription** → Far future expiration date
- ⏱️ **Trial** → 30 days from now
- ❌ **Expired/Invalid** → Past date or near-future date
- 🔗 **Already linked** → Warning about duplicate usage

---

## How to Stop This Ping

### Option 1: Disable the Cron Job

```sql
-- Find the cron job
SELECT id, name, active FROM ir_cron WHERE model_id IN (
    SELECT id FROM ir_model WHERE model = 'publisher_warranty.contract'
);

-- Disable it
UPDATE ir_cron
SET active = false
WHERE model_id IN (SELECT id FROM ir_model WHERE model = 'publisher_warranty.contract');
```

Or via Odoo UI:
1. Settings → Technical → Scheduled Actions
2. Search: "Publisher: Update Notification"
3. Click → Archive

### Option 2: Change the Target URL

Edit `odoo.conf`:
```ini
[options]
publisher_warranty_url = http://localhost:9999/fake
# Or completely disable:
publisher_warranty_url = False
```

This prevents your database from contacting Odoo servers.

### Option 3: Network-Level Block

Block outgoing connections to `services.odoo.com`:
```bash
# Firewall rule
sudo iptables -A OUTPUT -d services.odoo.com -j DROP
```

---

## Key Differences: Community vs Enterprise

| Aspect | Community Edition | Enterprise Edition |
|--------|------------------|-------------------|
| **Ping Happens?** | ✅ Yes, weekly | ✅ Yes, weekly |
| **Parameters Set?** | ✅ Yes | ✅ Yes |
| **Expiration Enforced?** | ❌ No | ✅ Yes |
| **Warnings Shown?** | ❌ No | ✅ Yes (30 days before) |
| **Access Blocked?** | ❌ Never | ✅ Yes (after expiration) |

### Why Community Still Pings

Even though Community doesn't enforce expiration:
- Odoo tracks usage statistics
- Detects if you should be using Enterprise
- Sends product announcements
- The system is unified (same codebase)

---

## Monitoring the Ping

### Check Last Ping Time

```sql
SELECT create_date, write_date, key, value
FROM ir_config_parameter
WHERE key IN ('database.expiration_date', 'database.expiration_reason');
```

The `write_date` shows when it was last updated (= last successful ping).

### Check Cron History

```sql
SELECT * FROM ir_cron
WHERE model_id = (SELECT id FROM ir_model WHERE model = 'publisher_warranty.contract')
ORDER BY id DESC;
```

### Enable Debug Logging

In `odoo.conf`:
```ini
[options]
log_level = debug
log_handler = odoo.addons.mail.models.update:DEBUG
```

Watch for:
```
DEBUG odoo.addons.mail.models.update: Sending publisher warranty request
DEBUG odoo.addons.mail.models.update: Received response: {...}
```

---

## Summary

**How Odoo Knows When to Expire:**

1. ⏰ **Weekly Cron** runs automatically
2. 📤 **Sends data** to `services.odoo.com/publisher-warranty/`
3. 🔍 **Odoo validates** your enterprise_code and subscription
4. 📥 **Receives** expiration_date and expiration_reason
5. 💾 **Stores** in `ir_config_parameter`
6. 🚨 **Enterprise module** checks and enforces expiration

**It's NOT just local subscription management - it actively pings Odoo's servers!**

To prevent expiration, you must either:
- 🏆 Get a valid enterprise subscription (proper way)
- 🔧 Use the tools I created (development/testing)
- 🚫 Block the ping mechanism (nuclear option)

---

## Configuration Reference

**Default Publisher Warranty URL** (`odoo/tools/config.py:78`):
```python
'publisher_warranty_url': 'http://services.odoo.com/publisher-warranty/'
```

**Cron Schedule** (`addons/mail/data/ir_cron_data.xml:22`):
```xml
<field name="interval_type">weeks</field>
<field name="interval_number">1</field>
```

**Parameters Updated**:
- `database.expiration_date`
- `database.expiration_reason`
- `database.enterprise_code`
- `database.already_linked_subscription_url`
- `database.already_linked_email`
- `database.already_linked_send_mail_url`
