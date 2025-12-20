# ChaosHub.lk Website Module for Odoo 18

> **Engineering Clarity from Chaos** - A complete, modern, SEO-optimized website module for Odoo 18.

---

## 📦 Module Information

- **Module Name**: ChaosHub.lk Website
- **Technical Name**: `chaos_chaoshublk`
- **Version**: 18.0.1.0.0
- **Category**: Website
- **License**: LGPL-3
- **Odoo Version**: 18.0 Community Edition

---

## ✨ Features

### 🎨 **Modern Design System**
- Gradient backgrounds with subtle animations
- Glassmorphism effects and smooth transitions
- Professional color scheme with CSS variables
- Card-based layouts with hover effects
- Responsive mobile-first design

### 📱 **Fully Responsive**
- Mobile-first design approach
- Works perfectly on all devices (phone, tablet, desktop)
- Touch-friendly buttons and forms
- Optimized grid layouts that stack on mobile

### 🔍 **SEO Optimized**
- Semantic HTML5 structure
- Complete meta tags for social sharing
- Schema.org structured data support
- Optimized heading hierarchy
- Fast loading performance

### ♿ **Accessible**
- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- High contrast ratios
- Proper focus indicators

### 📄 **Complete Page Set**
1. **Homepage** - Hero, About, Knowledge Base, Features, Articles, CTA, Newsletter
2. **About Us** - Company story, mission, vision, values
3. **Services** - Business solutions and offerings
4. **Contact** - Contact form with multiple channels
5. **News/Blog** - Latest insights and articles (integrates with Odoo Blog)
6. **Help/FAQ** - Frequently asked questions and support

---

## 🚀 Installation

### Prerequisites
- Odoo 18 Community Edition installed
- Access to Odoo addons directory
- Website module (comes with Odoo)
- Website Blog module (optional, for news section)

### Step 1: Copy Module to Addons Directory

```bash
# Navigate to your Odoo addons directory
cd /path/to/odoo/addons

# Copy the module
cp -r /path/to/chaos_chaoshublk ./

# Set proper permissions
chmod -R 755 chaos_chaoshublk
```

### Step 2: Update Apps List

```bash
# Restart Odoo server
sudo systemctl restart odoo

# OR if running manually
./odoo-bin -c /path/to/odoo.conf
```

In Odoo:
1. Go to **Apps** menu
2. Click **Update Apps List**
3. Remove the "Apps" filter (search all modules)
4. Search for "ChaosHub"

### Step 3: Install the Module

1. Find "ChaosHub.lk Website" in the apps list
2. Click **Install**
3. Wait for installation to complete

### Step 4: Verify Installation

1. Go to **Website** app
2. Visit your website
3. You should see the new ChaosHub homepage
4. Check the menu items (Home, Knowledge Base, Services, etc.)

---

## 📁 Module Structure

```
chaos_chaoshublk/
├── __init__.py                      # Python initialization
├── __manifest__.py                  # Module configuration
├── README.md                        # This file
│
├── static/
│   └── src/
│       ├── css/
│       │   └── chaoshub.css        # Complete design system CSS
│       ├── js/
│       │   └── chaoshub.js         # Frontend JavaScript
│       └── img/
│           └── (your images here)
│
├── views/
│   ├── homepage.xml                # Homepage template
│   ├── about.xml                   # About Us page
│   ├── services.xml                # Services page
│   ├── contact.xml                 # Contact page
│   ├── news.xml                    # News/Blog landing page
│   ├── help.xml                    # Help/FAQ page
│   └── templates.xml               # Common templates & footer
│
├── data/
│   └── website_data.xml            # Menu items configuration
│
└── security/
    └── ir.model.access.csv         # Access rights (minimal)
```

---

## 🎨 Customization Guide

### Change Color Scheme

Edit `static/src/css/chaoshub.css` and modify CSS variables:

```css
:root {
    /* Change these values */
    --color-primary: #6366f1;      /* Main brand color */
    --color-secondary: #ec4899;    /* Secondary color */
    --color-accent: #14b8a6;       /* Accent color */
}
```

All components will automatically update!

### Change Fonts

In `views/templates.xml`, update the Google Fonts link:

```xml
<link href="https://fonts.googleapis.com/css2?family=YourFont&display=swap" rel="stylesheet"/>
```

Then update CSS variables in `chaoshub.css`:

```css
:root {
    --font-heading: 'Your Font', sans-serif;
    --font-primary: 'Your Font', sans-serif;
}
```

### Replace Emoji Icons with Images

In any XML template, replace emoji icons:

```xml
<!-- Before (emoji) -->
<div class="card-icon">📊</div>

<!-- After (image) -->
<div class="card-icon">
    <img src="/chaos_chaoshublk/static/src/img/your-icon.png" alt="Icon"/>
</div>
```

### Update Content

Edit XML files in `views/` directory:
- `homepage.xml` - Homepage content
- `about.xml` - About Us content
- `services.xml` - Services descriptions
- `contact.xml` - Contact information
- `news.xml` - News page content
- `help.xml` - FAQ items

After editing, upgrade the module:
```bash
# In Odoo Apps menu
1. Search for "ChaosHub.lk Website"
2. Click "Upgrade"
```

---

## 🔗 URL Structure

After installation, these pages will be available:

- **Homepage**: `/` or `/home`
- **About Us**: `/aboutus`
- **Services**: `/services`
- **Contact**: `/contactus`
- **News**: `/news`
- **Blog**: `/blog` (Odoo Blog module)
- **Help**: `/help`

---

## 📋 Menu Configuration

The module creates these menu items automatically:

1. Home
2. Knowledge Base (links to /blog)
3. News
4. Services
5. About Us
6. Contact
7. Help

To customize menus:
1. Go to **Website → Site → Menus**
2. Edit any menu item
3. Change name, URL, or sequence

---

## 🛠️ Technical Details

### Dependencies
- `website` - Odoo Website module (required)
- `website_blog` - Odoo Blog module (optional)

### Assets
The module loads these assets automatically:
- `chaos_chaoshublk/static/src/css/chaoshub.css` - Complete CSS
- `chaos_chaoshublk/static/src/js/chaoshub.js` - Frontend JavaScript

### Models
This module doesn't create any custom models. It only extends:
- `website.page` - For page records
- `website.menu` - For menu items

---

## 🎯 SEO Configuration

### Per-Page Meta Tags

Each page template includes meta tags. To customize:

1. Open the page XML file (e.g., `views/homepage.xml`)
2. Add meta tags in the `<head>` section
3. Example:

```xml
<t t-call="website.layout">
    <t t-set="additional_title">Your Page Title | ChaosHub.lk</t>
    <t t-set="meta_description">Your page description here</t>
    <!-- Page content -->
</t>
```

### Sitemap

Odoo automatically generates a sitemap at `/sitemap.xml` including all published pages from this module.

---

## 📱 Responsive Breakpoints

The design system uses these breakpoints:

- **Desktop**: Default (1280px max container)
- **Tablet**: 768px and below
- **Mobile**: 480px and below

All layouts automatically stack on mobile devices.

---

## ♿ Accessibility Features

- Semantic HTML5 elements
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus indicators on all interactive elements
- High contrast text (WCAG AA compliant)
- Responsive images with alt text

---

## 🧪 Testing Checklist

After installation, verify:

- [ ] All pages load correctly
- [ ] Navigation menu appears on all pages
- [ ] Footer displays on all pages
- [ ] CSS styles load properly
- [ ] Forms work (newsletter, contact)
- [ ] Responsive design on mobile
- [ ] All links work
- [ ] No console errors

---

## 🐛 Troubleshooting

### CSS Not Loading

**Problem**: Styles not appearing correctly
**Solution**:
1. Clear browser cache (Ctrl + Shift + Delete)
2. Restart Odoo server
3. Check browser console for errors
4. Verify assets are loaded in Network tab

### Pages Not Appearing

**Problem**: Pages return 404 error
**Solution**:
1. Verify module is installed (Apps → ChaosHub.lk Website)
2. Check Website → Site → Pages (pages should be published)
3. Upgrade module if you made XML changes

### Menu Items Missing

**Problem**: Navigation menu is empty
**Solution**:
1. Go to Website → Site → Menus
2. Verify menu items exist
3. Check they're assigned to the correct website
4. Upgrade module to reload menu data

---

## 🔄 Updating the Module

### After Making Changes

1. Edit your XML, CSS, or JS files
2. Restart Odoo server (if Python changes)
3. Go to Apps menu in Odoo
4. Search for "ChaosHub.lk Website"
5. Click **Upgrade** button

### Force Upgrade from Command Line

```bash
./odoo-bin -c /path/to/odoo.conf -u chaos_chaoshublk -d your_database
```

---

## 📧 Support

For questions or issues with this module:

- **Email**: hello@chaoshub.lk
- **Website**: https://chaoshub.lk
- **Documentation**: See `../chaoshub_design_system.md`

---

## 📜 License

This module is licensed under LGPL-3.

---

## 🙏 Credits

**Created for**: ChaosHub.lk
**Date**: December 2025
**Odoo Version**: 18.0 Community Edition

**Fonts Used**:
- Sora by Julien Saurin (Google Fonts)
- Inter by Rasmus Andersson (Google Fonts)

---

## 🚀 Next Steps After Installation

1. **Customize Content**
   - Update company information in About page
   - Add your services to Services page
   - Update contact information

2. **Add Images**
   - Replace emoji icons with real images
   - Add company logo
   - Add team photos (if applicable)

3. **Configure Blog**
   - Install Blog module if not already installed
   - Create blog categories
   - Write first blog post

4. **Set Up Forms**
   - Configure email notifications for contact form
   - Test newsletter subscription
   - Set up form submission handling

5. **SEO Optimization**
   - Submit sitemap to Google Search Console
   - Set up Google Analytics
   - Create Open Graph images
   - Optimize meta descriptions

6. **Go Live**
   - Test all pages thoroughly
   - Check mobile responsiveness
   - Verify all links work
   - Announce your launch!

---

**Built with ❤️ for ChaosHub.lk**

*Engineering Clarity from Chaos*
