# How to Prevent Odoo Database Expiration

This guide provides multiple methods to prevent your Odoo database from expiring after 30 days.

## Understanding Database Expiration

- **Community Edition**: Expiration parameters exist but are NOT enforced. Your database won't actually expire.
- **Enterprise Edition**: Expiration is enforced. After the trial period or if your subscription expires, access may be restricted.

## Quick Check: Is Your Database Actually Expiring?

Run this to check your current status:

```bash
psql your_database_name -c "SELECT key, value FROM ir_config_parameter WHERE key IN ('database.expiration_date', 'database.expiration_reason', 'database.enterprise_code');"
```

---

## Method 1: SQL Direct Update (Fastest - 30 seconds)

**Best for**: Quick fix, immediate results

```bash
# Connect to your database
psql your_database_name -f extend_expiration.sql
```

Or manually:

```sql
-- Update expiration to 10 years from now
UPDATE ir_config_parameter
SET value = (CURRENT_DATE + INTERVAL '10 years')::text
WHERE key = 'database.expiration_date';

-- Clear expiration reason
UPDATE ir_config_parameter
SET value = ''
WHERE key = 'database.expiration_reason';
```

**Restart Odoo** after making changes for them to take effect.

---

## Method 2: Python Script (Recommended for remote databases)

**Best for**: Remote databases, automated management

```bash
# Check current expiration
python3 extend_database_expiration.py -d your_db -p your_password --check

# Extend expiration by 10 years
python3 extend_database_expiration.py -d your_db -p your_password -y 10
```

Full usage:
```bash
python3 extend_database_expiration.py \
  -u http://localhost:8069 \
  -d your_database \
  -U admin \
  -p your_password \
  -y 10
```

---

## Method 3: Install Custom Module (Permanent Solution)

**Best for**: Development environments, permanent fix

### Installation Steps:

1. **Restart Odoo with the module path:**
   ```bash
   ./odoo-bin -c odoo.conf -u base -d your_database
   ```

2. **Activate Developer Mode:**
   - Settings → Activate Developer Mode

3. **Update Apps List:**
   - Apps → Update Apps List

4. **Install the Module:**
   - Search for "Disable Database Expiration"
   - Click Install

### What This Module Does:

- ✓ Automatically extends expiration to 50 years
- ✓ Clears expiration warnings
- ✓ Runs daily to keep expiration extended
- ✓ Works on module installation and daily via cron

---

## Method 4: Disable Publisher Warranty Checks (Nuclear Option)

**Warning**: This prevents ALL update notifications

Edit your `odoo.conf`:

```ini
[options]
# Disable publisher warranty checks (no expiration updates from Odoo servers)
publisher_warranty_url = False
```

Or start Odoo with:
```bash
./odoo-bin --publisher_warranty_url=False
```

---

## Method 5: Odoo Shell Interactive Update

```bash
# Start Odoo shell
./odoo-bin shell -d your_database

# In the shell:
from datetime import datetime, timedelta
env['ir.config_parameter'].sudo().set_param('database.expiration_date', (datetime.now() + timedelta(days=3650)).strftime('%Y-%m-%d'))
env['ir.config_parameter'].sudo().set_param('database.expiration_reason', '')
env.cr.commit()
exit()
```

---

## Verification

After applying any method, verify the changes:

### Via SQL:
```bash
psql your_database -c "SELECT key, value FROM ir_config_parameter WHERE key = 'database.expiration_date';"
```

### Via Odoo Interface:
1. Settings → Technical → Parameters → System Parameters
2. Look for `database.expiration_date`
3. Should show a date far in the future

### Via Web Interface:
1. Settings → General Settings
2. Scroll to "About" section
3. Check the expiration date displayed

---

## Important Notes

### For Community Edition Users:
- Your database **doesn't actually expire**
- These parameters are informational only
- No action is strictly necessary

### For Enterprise Edition Users:
- **Proper Solution**: Get a valid enterprise subscription from Odoo
- **Development/Testing**: Use the methods above
- **Production**: Always use a valid license

### After Updates:
- The publisher warranty cron may reset your expiration date
- The custom module (Method 3) will automatically re-extend it
- Or disable the cron: Settings → Technical → Scheduled Actions → "Update Notification" → Deactivate

---

## Troubleshooting

### Changes Don't Take Effect:
```bash
# Restart Odoo
sudo systemctl restart odoo
# or
./odoo-bin -c odoo.conf
```

### Still Seeing Warnings:
1. Clear browser cache
2. Check if `web_enterprise` module is installed
3. Verify changes in database directly

### Expiration Keeps Resetting:
Disable the update notification cron:
```sql
UPDATE ir_cron
SET active = false
WHERE model_id IN (SELECT id FROM ir_model WHERE model = 'publisher_warranty.contract');
```

---

## Files Created

- `extend_database_expiration.py` - Python script for extending expiration
- `extend_expiration.sql` - SQL script for direct database update
- `addons/disable_expiration/` - Odoo module for permanent solution

## Quick Reference

| Method | Time | Difficulty | Permanent | Best For |
|--------|------|------------|-----------|----------|
| SQL Direct | 30s | Easy | No | Quick fix |
| Python Script | 1min | Easy | No | Remote DBs |
| Custom Module | 5min | Medium | Yes | Dev environments |
| Disable Updates | 30s | Easy | Yes | Nuclear option |
| Odoo Shell | 2min | Medium | No | One-off updates |

---

**Need Help?** Check the current expiration status first:
```bash
python3 extend_database_expiration.py -d your_db -p password --check
```
