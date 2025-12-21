# ChaosHub.lk - Professional Odoo 18 Website Module

> **Enterprise-Grade Knowledge Hub with Website Builder Integration, SEO, and Custom Snippets**

Version: 18.0.2.0.0 | License: LGPL-3 | Odoo: 18.0 Community/Enterprise

---

## 🌟 Overview

ChaosHub.lk is a **production-ready, professional Odoo 18 website module** designed following best practices from the Odoo Enterprise codebase. This module provides a complete knowledge-sharing platform with:

- **Drag-and-Drop Website Builder Snippets**
- **Advanced SEO with JSON-LD Structured Data**
- **Dynamic Blog/Knowledge Base System**
- **Professional SCSS Architecture with Variables & Mixins**
- **Modern JavaScript (ES6+ Modules)**
- **Full i18n Translation Support**

---

## 📦 What's New in Version 2.0

### ✨ **Website Builder Integration**
- Custom snippets for drag-and-drop page building
- Hero sections with multiple style variations
- Features grid with customizable layouts
- Dynamic blog cards that pull latest posts
- Newsletter subscription with AJAX handling
- CTA banners with full-width options

### 🎨 **Professional SCSS Architecture**
- Variables file for design system consistency
- Mixins for reusable styling patterns
- Modular SCSS structure (variables, mixins, main, snippets)
- Responsive breakpoint mixins
- Button and card component mixins

### 🔍 **Advanced SEO**
- JSON-LD structured data for articles
- Organization and Website schema
- Automatic meta tag generation per page
- Open Graph and Twitter Card support
- Enhanced sitemap with blog posts
- Reading time calculation

### 🚀 **Dynamic Controllers**
- Knowledge base with pagination & search
- Category filtering for articles
- Single article view with related posts
- Newsletter subscription endpoint (JSON-RPC)
- SEO meta tag helpers

### 📱 **Enhanced UX**
- Smooth scroll for anchor links
- Lazy loading images with Intersection Observer
- AJAX newsletter subscriptions
- Social sharing buttons
- Related articles recommendations

---

## 🏗️ Architecture

### **Module Structure**

```
chaos_chaoshublk/
├── __init__.py                      # Module initialization
├── __manifest__.py                  # Module configuration
├── README_PROFESSIONAL.md           # This file
│
├── controllers/
│   ├── __init__.py
│   └── main.py                      # Dynamic controllers (Knowledge, Newsletter, SEO)
│
├── models/
│   ├── __init__.py
│   └── website.py                   # Website & BlogPost extensions
│
├── views/
│   ├── homepage.xml                 # Homepage template
│   ├── about.xml                    # About Us page
│   ├── services.xml                 # Services page
│   ├── contact.xml                  # Contact page
│   ├── help.xml                     # Help/FAQ page
│   ├── knowledge_base.xml          # Dynamic knowledge base listing
│   ├── article_detail.xml          # Single article with SEO
│   ├── blog_views.xml              # Blog model extensions
│   ├── templates.xml               # Common templates & footer
│   ├── seo_templates.xml           # SEO meta tags & schema
│   │
│   └── snippets/
│       ├── snippets.xml            # Snippet registration
│       ├── s_chaoshub_hero.xml     # Hero snippet
│       ├── s_chaoshub_features.xml # Features grid
│       ├── s_chaoshub_blog_cards.xml # Blog cards
│       ├── s_chaoshub_cta.xml      # CTA banner
│       └── s_chaoshub_newsletter.xml # Newsletter form
│
├── static/src/
│   ├── scss/
│   │   ├── variables.scss          # Design system variables
│   │   ├── mixins.scss             # Reusable mixins
│   │   ├── chaoshub.scss           # Main styles
│   │   └── snippets.scss           # Snippet-specific styles
│   │
│   ├── js/
│   │   ├── chaoshub.js             # Main frontend JS
│   │   ├── snippets.js             # Snippet interactions
│   │   ├── newsletter.js           # Newsletter AJAX handler
│   │   └── snippet_options.js      # Builder options
│   │
│   └── img/
│       └── snippets/               # Snippet thumbnails
│
├── data/
│   └── website_data.xml            # Menu items
│
└── security/
    └── ir.model.access.csv         # Access rights
```

---

## 🎯 Key Features

### **1. Website Builder Snippets**

All snippets are accessible from the **Website Builder** (Edit Mode → Building Blocks → ChaosHub Components):

#### **Hero Section (`s_chaoshub_hero`)**
- Multiple style variations (Gradient, Solid, Image)
- Adjustable height (Small 60vh, Default 100vh, Large 120vh)
- Editable badge, title, subtitle, and CTA buttons
- Fully responsive

#### **Features Grid (`s_chaoshub_features`)**
- 2, 3, or 4 column layouts
- Icon + Title + Description cards
- Hover animations
- Customizable through Website Builder

#### **Blog Cards (`s_chaoshub_blog_cards`)**
- Dynamically loads latest blog posts
- Shows categories, reading time, featured image
- Responsive grid layout
- Automatic linking to article pages

#### **CTA Banner (`s_chaoshub_cta`)**
- Eye-catching call-to-action section
- Gradient background with animations
- Primary + Secondary button options
- Full-width toggle option

#### **Newsletter (`s_chaoshub_newsletter`)**
- AJAX form submission (no page reload)
- Success/error message handling
- Email validation
- Integrates with Odoo mass_mailing

---

### **2. SEO Optimization**

#### **Automatic Meta Tags**
Every page includes:
- Title tag (unique per page)
- Meta description
- Meta keywords
- Open Graph tags (Facebook, LinkedIn)
- Twitter Card tags
- Canonical URLs

#### **JSON-LD Structured Data**
- **Article Schema** for blog posts
- **Organization Schema** for company info
- **Website Schema** with search functionality
- Improves search engine understanding and rich snippets

#### **Enhanced Sitemap**
- Automatically includes all blog posts
- Priority and change frequency for each page
- Helps search engines discover content

---

### **3. Dynamic Knowledge Base**

**URL**: `/knowledge`

Features:
- **Category Filtering** - Filter by blog tags
- **Search Functionality** - Search article titles and content
- **Pagination** - 12 articles per page
- **Responsive Grid** - 3 columns on desktop, stacks on mobile
- **Reading Time** - Calculated automatically (200 words/min)
- **Featured Images** - Fallback to emoji icons

---

### **4. Article Detail Page**

**URL**: `/article/<slug>`

Features:
- **SEO-Optimized Header** with meta tags
- **JSON-LD Structured Data** (Article schema)
- **Cover Image** with lazy loading
- **Author & Date** information
- **Reading Time** display
- **Category Tags** with links
- **Social Sharing** (Twitter, LinkedIn)
- **Related Articles** (3 posts with similar tags)
- **Newsletter CTA** at bottom

---

### **5. Professional Design System**

#### **SCSS Variables** (`variables.scss`)
```scss
// Colors
$color-primary: #6366f1;
$color-secondary: #ec4899;
$color-accent: #14b8a6;

// Typography
$font-heading: 'Sora';
$font-primary: 'Inter';

// Spacing
$space-4: 1rem;
$space-8: 2rem;

// Breakpoints
$breakpoint-md: 768px;
$breakpoint-lg: 1024px;
```

#### **SCSS Mixins** (`mixins.scss`)
```scss
@include btn-primary;
@include card;
@include text-gradient;
@include respond-to('md');
```

---

## 🚀 Installation

### **Prerequisites**
- Odoo 18.0 (Community or Enterprise)
- `website` module (comes with Odoo)
- `website_blog` module (comes with Odoo)
- `mass_mailing` module (comes with Odoo)

### **Step 1: Install Module**

```bash
# Copy module to Odoo addons directory
cp -r chaos_chaoshublk /opt/odoo/addons/

# Set permissions
sudo chown -R odoo:odoo /opt/odoo/addons/chaos_chaoshublk
sudo chmod -R 755 /opt/odoo/addons/chaos_chaoshublk

# Restart Odoo
sudo systemctl restart odoo
```

### **Step 2: Activate in Odoo**

1. Go to **Apps** menu
2. Click **Update Apps List**
3. Search for "**ChaosHub**"
4. Click **Install**

### **Step 3: Configure Blog**

1. Go to **Website → Blog → Blogs**
2. Create a new blog or use existing
3. Create blog posts with:
   - Title, subtitle, content
   - Cover image
   - Tags/categories
   - Set as "Published"

### **Step 4: Use Website Builder**

1. Go to **Website** app
2. Click any page → **Edit**
3. Drag ChaosHub snippets from **Building Blocks**
4. Customize content inline
5. Click **Save**

---

## 🎨 Customization

### **Change Colors**

Edit `static/src/scss/variables.scss`:

```scss
$color-primary: #YOUR-COLOR;
$color-secondary: #YOUR-COLOR;
$color-accent: #YOUR-COLOR;
```

Then restart Odoo and clear assets:
```bash
# Clear assets
odoo-bin --stop-after-init -d your_db --update chaos_chaoshublk
```

### **Add Custom Snippets**

1. Create new snippet XML in `views/snippets/`
2. Register in `views/snippets/snippets.xml`
3. Add styles in `static/src/scss/snippets.scss`
4. Add JS options in `static/src/js/snippet_options.js`
5. Upgrade module

### **Modify Page Templates**

1. Edit XML files in `views/`
2. Use `<t t-call="template_name"/>` for reusable blocks
3. Upgrade module to apply changes

---

## 📊 SEO Best Practices

### **For Each Blog Post:**
1. **Write compelling title** (50-60 characters)
2. **Add subtitle** (becomes meta description)
3. **Upload cover image** (1200x630px recommended)
4. **Add relevant tags** (helps categorization)
5. **Choose schema type** (Article, BlogPosting, TechArticle, HowTo)

### **Content Guidelines:**
- Write 800+ words for better SEO
- Use headings (H2, H3) for structure
- Include images with alt text
- Link to related articles internally
- Add schema.org markup

### **Technical SEO:**
- Module automatically handles sitemap
- Meta tags generated per page
- JSON-LD structured data included
- Open Graph tags for social sharing
- Mobile-responsive (Google requirement)

---

## 🧪 Testing Checklist

After installation, verify:

- [ ] Homepage loads correctly
- [ ] All menu items work
- [ ] Knowledge base shows blog posts
- [ ] Article detail page displays
- [ ] Search functionality works
- [ ] Category filtering works
- [ ] Newsletter form submits
- [ ] Snippets appear in Website Builder
- [ ] Snippets are draggable
- [ ] Mobile responsive on all pages
- [ ] SEO meta tags present (view source)
- [ ] JSON-LD schema validates (Google Rich Results Test)
- [ ] Sitemap includes blog posts (`/sitemap.xml`)

---

## 🐛 Troubleshooting

### **Snippets Not Appearing**
- Ensure module is fully installed
- Clear browser cache (Ctrl+Shift+Delete)
- Regenerate assets: Settings → Technical → Assets → Regenerate

### **SCSS Not Compiling**
- Check Odoo logs for syntax errors
- Ensure all `@import` statements are correct
- Restart Odoo server

### **Newsletter Not Working**
- Check `mass_mailing` module is installed
- Verify CSRF token in form
- Check browser console for JS errors

### **Blog Posts Not Showing**
- Ensure posts are published (`website_published = True`)
- Check blog is assigned to current website
- Verify posts have content

---

## 📚 Documentation

### **For Developers:**
- **Python Controllers**: `controllers/main.py`
- **Models**: `models/website.py`
- **SCSS Variables**: `static/src/scss/variables.scss`
- **Mixins**: `static/src/scss/mixins.scss`

### **For Content Creators:**
- Use Website Builder for page editing
- Create blog posts in Website → Blog
- Use snippets for consistent design
- Follow SEO guidelines above

### **For Designers:**
- Customize `variables.scss` for branding
- Modify snippet templates in `views/snippets/`
- Add custom CSS in `chaoshub.scss`

---

## 🔄 Upgrade Path

### **From Version 1.0 to 2.0:**

1. **Backup database**
2. **Copy new module** files
3. **Upgrade module**:
   ```bash
   odoo-bin -u chaos_chaoshublk -d your_db
   ```
4. **Clear assets**
5. **Test website**

---

## 📖 Additional Resources

- [Odoo Website Builder Documentation](https://www.odoo.com/documentation/18.0/applications/websites.html)
- [Odoo Blog Documentation](https://www.odoo.com/documentation/18.0/applications/websites/blog.html)
- [Schema.org Markup](https://schema.org/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)

---

## 🤝 Support & Contribution

### **Issues & Bugs**
Report issues on the project repository with:
- Odoo version
- Module version
- Steps to reproduce
- Error logs

### **Feature Requests**
We welcome feature requests! Please describe:
- Use case
- Expected behavior
- Why it's valuable

---

## 📝 License

This module is licensed under **LGPL-3**.

---

## 🙏 Credits

**Created for**: ChaosHub.lk
**Version**: 2.0.0
**Date**: December 2025
**Odoo Version**: 18.0 Community/Enterprise

**Technologies**:
- Odoo Website Builder
- SCSS (Sass)
- JavaScript (ES6+ Modules)
- JSON-LD (Schema.org)
- Python (Odoo ORM)

**Fonts**:
- Sora (Google Fonts)
- Inter (Google Fonts)

---

**Built with ❤️ following Odoo Enterprise best practices**

*Engineering Clarity from Chaos*
