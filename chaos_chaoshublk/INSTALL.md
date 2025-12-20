# Quick Installation Guide - ChaosHub.lk Website Module

## 🚀 5-Minute Installation

### Step 1: Copy Module (1 minute)

```bash
# Copy module to Odoo addons directory
cp -r chaos_chaoshublk /path/to/odoo/addons/

# Example paths:
# Ubuntu: /opt/odoo/addons/
# Custom: /path/to/your/odoo/addons/
```

### Step 2: Set Permissions (30 seconds)

```bash
# Set proper ownership and permissions
sudo chown -R odoo:odoo /path/to/odoo/addons/chaos_chaoshublk
sudo chmod -R 755 /path/to/odoo/addons/chaos_chaoshublk
```

### Step 3: Restart Odoo (1 minute)

```bash
# If using systemd
sudo systemctl restart odoo

# OR manually
sudo service odoo restart

# OR if running Odoo directly
# Stop current process (Ctrl+C) and restart:
./odoo-bin -c /path/to/odoo.conf
```

### Step 4: Update Apps List (1 minute)

1. Open Odoo in your browser
2. Log in as Administrator
3. Go to **Apps** menu (top navigation)
4. Click **Update Apps List** (⋮ menu → Update Apps List)
5. Click **Update** in the confirmation dialog
6. Wait for the process to complete

### Step 5: Install Module (2 minutes)

1. In the Apps menu, remove the "Apps" filter
   - Click the **X** next to "Apps" in the search
2. Search for "**ChaosHub**"
3. Find "**ChaosHub.lk Website**" module
4. Click **Install** button
5. Wait for installation (should take 30-60 seconds)

---

## ✅ Verify Installation

### Check Website

1. Go to **Website** app (from main menu)
2. Click **Go to Website** button
3. You should see the new ChaosHub homepage
4. Check navigation menu has all items:
   - Home
   - Knowledge Base
   - News
   - Services
   - About Us
   - Contact
   - Help

### Check Pages

Visit these URLs to verify all pages work:
- `http://your-domain/` - Homepage
- `http://your-domain/aboutus` - About Us
- `http://your-domain/services` - Services
- `http://your-domain/contactus` - Contact
- `http://your-domain/news` - News
- `http://your-domain/help` - Help

---

## 🎨 First Customizations

### 1. Update Contact Information

Edit `views/contact.xml`:

```xml
<!-- Find and update -->
<p>hello@chaoshub.lk</p>  <!-- Change email -->
<p>+94 XX XXX XXXX</p>    <!-- Change phone -->
```

After editing:
1. Go to Apps
2. Search "ChaosHub"
3. Click **Upgrade**

### 2. Change Colors

Edit `static/src/css/chaoshub.css`:

```css
:root {
    --color-primary: #YOUR-COLOR;
    --color-secondary: #YOUR-COLOR;
}
```

Refresh your browser (Ctrl+F5)

### 3. Add Your Logo

Replace emoji icon in `views/templates.xml`:

```xml
<div class="footer-logo">
    <img src="/path/to/logo.png" alt="ChaosHub"/>
</div>
```

---

## 📊 Quick Reference

### Module Location
```
/path/to/odoo/addons/chaos_chaoshublk/
```

### Key Files to Customize
```
views/contact.xml       → Contact info
views/about.xml         → Company story
views/services.xml      → Services offered
static/src/css/chaoshub.css → Colors, fonts
```

### Restart & Upgrade Commands
```bash
# Restart Odoo
sudo systemctl restart odoo

# Upgrade module from CLI
./odoo-bin -c odoo.conf -u chaos_chaoshublk -d database_name
```

---

## 🐛 Common Issues

### Module Not Appearing in Apps List

**Solution**:
1. Verify module is in correct addons directory
2. Check `__manifest__.py` exists and has no syntax errors
3. Restart Odoo server
4. Update Apps List again

### CSS Not Loading

**Solution**:
1. Hard refresh browser (Ctrl+Shift+R)
2. Clear browser cache
3. Check browser console for errors (F12)
4. Verify file exists: `static/src/css/chaoshub.css`

### Pages Return 404

**Solution**:
1. Verify module is fully installed
2. Check Website → Site → Pages
3. Ensure pages are published (green toggle)
4. Try upgrading the module

### Menu Items Not Showing

**Solution**:
1. Go to Website → Site → Menus
2. Check menu items exist
3. Verify sequence numbers are correct
4. Ensure they're assigned to your website

---

## 📞 Need Help?

- **Full Documentation**: See `README.md` in module directory
- **Design Guide**: See `../chaoshub_design_system.md`
- **Quick Reference**: See `../QUICK_REFERENCE.md`
- **Email**: hello@chaoshub.lk

---

## 🎉 Success!

If you can see the ChaosHub homepage with all menu items working, you're done!

**Next Steps**:
1. Customize content for your business
2. Add your branding (logo, colors)
3. Create blog posts
4. Set up Google Analytics
5. Submit sitemap to Google

**Enjoy your new website!** 🚀
