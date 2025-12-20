# ChaosHub.lk - Quick Reference Guide

> Copy-paste ready code snippets for common components

---

## 🎨 Color Customization

### Change Primary Color
```css
:root {
    --color-primary: #6366f1;  /* Change this */
}
```

### Popular Color Schemes

**Blue (Default)**
```css
--color-primary: #6366f1;
--color-secondary: #ec4899;
--color-accent: #14b8a6;
```

**Green/Nature**
```css
--color-primary: #10b981;
--color-secondary: #8b5cf6;
--color-accent: #f59e0b;
```

**Purple/Creative**
```css
--color-primary: #8b5cf6;
--color-secondary: #ec4899;
--color-accent: #06b6d4;
```

**Orange/Energy**
```css
--color-primary: #f97316;
--color-secondary: #06b6d4;
--color-accent: #10b981;
```

---

## 🔘 Buttons

### Primary Button
```html
<a href="/link" class="btn btn-primary">Click Me</a>
```

### Secondary Button
```html
<a href="/link" class="btn btn-secondary">Learn More</a>
```

### Large Button
```html
<a href="/link" class="btn btn-primary btn-lg">Get Started</a>
```

### Button Group
```html
<div style="display: flex; gap: 1rem; flex-wrap: wrap;">
    <a href="#" class="btn btn-primary">Primary</a>
    <a href="#" class="btn btn-secondary">Secondary</a>
</div>
```

---

## 📦 Cards

### Basic Card
```html
<div class="card">
    <h3 class="card-title">Card Title</h3>
    <p class="card-text">Card description goes here.</p>
</div>
```

### Card with Icon
```html
<div class="card">
    <div class="card-icon">📊</div>
    <h3 class="card-title">ERP Solutions</h3>
    <p class="card-text">Streamline your business operations.</p>
</div>
```

### Card with Button
```html
<div class="card">
    <div class="card-icon">💡</div>
    <h3 class="card-title">Service Name</h3>
    <p class="card-text">Service description here.</p>
    <a href="/service" class="btn btn-primary">Learn More</a>
</div>
```

### Knowledge Card (with top border animation)
```html
<div class="card knowledge-card">
    <div class="card-icon">🎓</div>
    <h3 class="card-title">Topic Name</h3>
    <p class="card-text">Topic description.</p>
</div>
```

---

## 📰 Article Cards

### Article Card
```html
<article class="article-card">
    <div class="article-image">📚</div>
    <div class="article-content">
        <div class="article-meta">
            <span class="article-tag">Category</span>
            <span>5 min read</span>
        </div>
        <h3 class="article-title">Article Title Here</h3>
        <p class="article-excerpt">
            Brief excerpt of the article content goes here...
        </p>
        <a href="/article-link" class="article-link">Read More →</a>
    </div>
</article>
```

### Article Grid (3 columns)
```html
<div class="grid grid-3">
    <article class="article-card">...</article>
    <article class="article-card">...</article>
    <article class="article-card">...</article>
</div>
```

---

## 📐 Grid Layouts

### 2 Column Grid
```html
<div class="grid grid-2">
    <div class="card">Column 1</div>
    <div class="card">Column 2</div>
</div>
```

### 3 Column Grid
```html
<div class="grid grid-3">
    <div class="card">Column 1</div>
    <div class="card">Column 2</div>
    <div class="card">Column 3</div>
</div>
```

### 4 Column Grid
```html
<div class="grid grid-4">
    <div class="card">Column 1</div>
    <div class="card">Column 2</div>
    <div class="card">Column 3</div>
    <div class="card">Column 4</div>
</div>
```

---

## 📑 Section Templates

### Section with Header
```html
<section class="section">
    <div class="container">
        <div class="section-header">
            <span class="section-badge">Category</span>
            <h2 class="section-title">Section Title</h2>
            <p class="section-description">
                Section description goes here.
            </p>
        </div>

        <!-- Content goes here -->
    </div>
</section>
```

### Alternate Background Section
```html
<section class="section section-alt">
    <div class="container">
        <h2>Section on Gray Background</h2>
        <p>Content here...</p>
    </div>
</section>
```

---

## 🎯 Hero Sections

### Full Height Hero
```html
<section class="hero">
    <div class="container">
        <div class="hero-content">
            <span class="hero-badge">Tagline</span>
            <h1>Main Headline</h1>
            <p class="hero-subtext">
                Supporting text that explains your value proposition.
            </p>
            <div class="hero-cta">
                <a href="/action" class="btn btn-primary btn-lg">Primary CTA</a>
                <a href="/secondary" class="btn btn-secondary btn-lg">Secondary CTA</a>
            </div>
        </div>
    </div>
</section>
```

### Shorter Hero (60vh)
```html
<section class="hero" style="min-height: 60vh;">
    <div class="container">
        <div class="hero-content">
            <span class="hero-badge">Page Category</span>
            <h1>Page Title</h1>
            <p class="hero-subtext">Page description.</p>
        </div>
    </div>
</section>
```

---

## 📢 CTA Banners

### CTA Banner
```html
<div class="cta-banner">
    <div class="cta-content">
        <h2>Call to Action Title</h2>
        <p>Compelling message encouraging user action.</p>
        <div class="cta-buttons">
            <a href="#" class="btn btn-primary btn-lg">Primary Action</a>
            <a href="#" class="btn btn-secondary btn-lg">Secondary Action</a>
        </div>
    </div>
</div>
```

### Full-Width CTA Section
```html
<section class="section">
    <div class="container">
        <div class="cta-banner">
            <div class="cta-content">
                <h2>Ready to Get Started?</h2>
                <p>Join thousands of businesses transforming chaos into clarity.</p>
                <a href="/signup" class="btn btn-primary btn-lg">Get Started Now</a>
            </div>
        </div>
    </div>
</section>
```

---

## ✉️ Forms

### Newsletter Form
```html
<div class="newsletter">
    <h3>Subscribe to Our Newsletter</h3>
    <p>Get the latest updates delivered to your inbox.</p>
    <form class="newsletter-form" action="/subscribe" method="POST">
        <input
            type="email"
            class="newsletter-input"
            placeholder="Enter your email"
            required
            name="email"
            aria-label="Email address"
        >
        <button type="submit" class="btn btn-primary">Subscribe</button>
    </form>
</div>
```

### Contact Form (Basic)
```html
<form action="/contact" method="POST">
    <div style="margin-bottom: 1rem;">
        <label for="name">Name</label>
        <input
            type="text"
            id="name"
            name="name"
            class="newsletter-input"
            style="width: 100%;"
            required
        >
    </div>

    <div style="margin-bottom: 1rem;">
        <label for="email">Email</label>
        <input
            type="email"
            id="email"
            name="email"
            class="newsletter-input"
            style="width: 100%;"
            required
        >
    </div>

    <div style="margin-bottom: 1rem;">
        <label for="message">Message</label>
        <textarea
            id="message"
            name="message"
            class="newsletter-input"
            style="width: 100%; min-height: 150px;"
            required
        ></textarea>
    </div>

    <button type="submit" class="btn btn-primary" style="width: 100%;">
        Send Message
    </button>
</form>
```

---

## 🖼️ Image Placeholders

### Replace Emoji with Image
```html
<!-- Before (emoji) -->
<div class="card-icon">📊</div>

<!-- After (image) -->
<div class="card-icon">
    <img src="/path/to/icon.png" alt="Icon description" style="width: 100%; height: 100%; object-fit: contain;">
</div>
```

### Article Image
```html
<!-- Before (emoji) -->
<div class="article-image">📚</div>

<!-- After (image) -->
<div class="article-image" style="background-image: url('/path/to/image.jpg'); background-size: cover; background-position: center;">
</div>
```

### About Section Visual
```html
<!-- Before (emoji) -->
<div class="about-visual">
    <div class="about-icon">🚀</div>
</div>

<!-- After (image) -->
<div class="about-visual" style="background-image: url('/path/to/image.jpg'); background-size: cover;">
</div>
```

---

## 🎨 Typography

### Headings
```html
<h1>Main Page Title (only one per page)</h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>
<h4>Card or Small Section Title</h4>
```

### Text with Gradient
```html
<h2 class="text-gradient">Gradient Text</h2>
```

### Centered Text
```html
<div class="text-center">
    <h2>Centered Heading</h2>
    <p>Centered paragraph.</p>
</div>
```

---

## 🔗 Links

### Regular Link
```html
<a href="/page">Link Text</a>
```

### External Link (opens in new tab)
```html
<a href="https://external-site.com" target="_blank" rel="noopener">
    External Link
</a>
```

### Link with Arrow
```html
<a href="/page" class="article-link">
    Read More →
</a>
```

---

## 📱 Responsive Utilities

### Hide on Mobile
```html
<div style="display: block;">
    <div style="display: none;">Visible on desktop only</div>
</div>

<!-- Better approach with media query -->
<style>
@media (max-width: 768px) {
    .hide-mobile { display: none; }
}
</style>
<div class="hide-mobile">Desktop only</div>
```

### Stack on Mobile
```html
<!-- Automatically stacks on mobile with grid classes -->
<div class="grid grid-2">
    <div>Column 1</div>
    <div>Column 2</div>
</div>
```

---

## 🎨 Custom Spacing

### Add Top Margin
```html
<div class="mt-8">Content with top margin</div>
```

### Add Bottom Margin
```html
<div class="mb-8">Content with bottom margin</div>
```

### Custom Spacing
```html
<div style="margin-top: var(--space-12);">Custom spacing</div>
```

---

## 🔍 SEO Meta Tags Template

### Homepage
```html
<head>
    <title>ChaosHub.lk - Your Journey Starts Here | ERP & Business Knowledge</title>
    <meta name="description" content="ChaosHub transforms complex business and technology concepts into clear, practical knowledge. Learn ERP, accounting, and digital transformation.">
    <meta name="keywords" content="ERP, accounting, digital transformation, business management, Odoo">
</head>
```

### Blog Post
```html
<head>
    <title>Article Title | ChaosHub.lk</title>
    <meta name="description" content="Brief article summary (150-160 characters)">
    <meta property="og:title" content="Article Title">
    <meta property="og:description" content="Article summary">
    <meta property="og:image" content="https://chaoshub.lk/images/article-image.jpg">
</head>
```

---

## 🎯 Common Patterns

### Two Column Layout (Text + Image)
```html
<div class="about-grid">
    <div class="about-content">
        <h2>Section Title</h2>
        <p>Content here...</p>
        <a href="/link" class="btn btn-primary">CTA Button</a>
    </div>
    <div class="about-visual">
        <div class="about-icon">🚀</div>
    </div>
</div>
```

### Feature Grid with Icons
```html
<div class="grid grid-3">
    <div class="card feature-card">
        <div class="feature-icon">✓</div>
        <h3 class="card-title">Feature Name</h3>
        <p class="card-text">Feature description.</p>
    </div>
    <!-- Repeat for more features -->
</div>
```

### Testimonial (Simple)
```html
<div class="card" style="text-align: center;">
    <p style="font-size: 1.25rem; font-style: italic; margin-bottom: 1rem;">
        "This is an amazing service that helped us grow our business!"
    </p>
    <p style="font-weight: 600; color: var(--color-dark);">
        John Doe
    </p>
    <p style="color: var(--color-gray); font-size: 0.875rem;">
        CEO, Company Name
    </p>
</div>
```

---

## 🔧 Odoo-Specific

### Link to Odoo Page
```html
<a href="/page/your-page-name">Link to Odoo Page</a>
```

### Link to Blog Post
```html
<a href="/blog/slug-name-1">Blog Post Title</a>
```

### Link to Product
```html
<a href="/shop/product/product-name-123">Product Name</a>
```

### Odoo Form Integration
```html
<form action="/website/form/contactus" method="POST">
    <!-- Form fields -->
</form>
```

---

## 📋 Quick Copy Sections

### Complete Section with Cards
```html
<section class="section">
    <div class="container">
        <div class="section-header">
            <span class="section-badge">Services</span>
            <h2 class="section-title">What We Offer</h2>
            <p class="section-description">
                Comprehensive solutions for your business needs.
            </p>
        </div>

        <div class="grid grid-3">
            <div class="card">
                <div class="card-icon">🎯</div>
                <h3 class="card-title">Service 1</h3>
                <p class="card-text">Service description here.</p>
            </div>

            <div class="card">
                <div class="card-icon">⚡</div>
                <h3 class="card-title">Service 2</h3>
                <p class="card-text">Service description here.</p>
            </div>

            <div class="card">
                <div class="card-icon">🚀</div>
                <h3 class="card-title">Service 3</h3>
                <p class="card-text">Service description here.</p>
            </div>
        </div>
    </div>
</section>
```

---

## 🎨 Icon Alternatives

Instead of emojis, you can use:

1. **Font Awesome** (Add in `<head>`)
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Then use -->
<div class="card-icon">
    <i class="fas fa-chart-line"></i>
</div>
```

2. **SVG Icons**
```html
<div class="card-icon">
    <svg>...</svg>
</div>
```

3. **Image Icons**
```html
<div class="card-icon">
    <img src="/icon.png" alt="Icon">
</div>
```

---

## 💡 Pro Tips

### Tip 1: Use Container for Width Control
```html
<section class="section">
    <div class="container">
        <!-- Content auto-centers with max-width -->
    </div>
</section>
```

### Tip 2: Alternate Section Backgrounds
```html
<section class="section">White background</section>
<section class="section section-alt">Gray background</section>
<section class="section">White background</section>
```

### Tip 3: Button Width on Mobile
```html
<!-- Full width on mobile, auto on desktop -->
<a href="#" class="btn btn-primary" style="width: 100%; max-width: 300px;">
    Button Text
</a>
```

### Tip 4: Lazy Load Images
```html
<img src="image.jpg" alt="Description" loading="lazy">
```

### Tip 5: Add Spacing Between Sections
```html
<section class="section" style="padding-top: 6rem;">
    <!-- Extra spacing -->
</section>
```

---

## 🔍 Finding Elements to Edit

### In Odoo Edit Mode:
1. Click "Edit" button
2. Hover over element you want to change
3. Click to select
4. Use sidebar to edit properties
5. Or click "Source Code" to edit HTML directly

### Using Browser DevTools:
1. Right-click element
2. Select "Inspect"
3. See HTML and CSS
4. Copy class names to reference this guide

---

## 📞 Need More Help?

Refer to:
- **Complete components**: `chaoshub_design_system.md`
- **Page templates**: `chaoshub_design_system.md`
- **Implementation steps**: `IMPLEMENTATION_CHECKLIST.md`
- **Overview**: `README_CHAOSHUB.md`

---

**Created for ChaosHub.lk | Version 1.0.0 | December 2025**