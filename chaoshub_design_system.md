# ChaosHub.lk Design System & Implementation Guide

## 📋 Table of Contents
1. [Quick Start - Odoo 18 Implementation](#quick-start)
2. [Design System Overview](#design-system)
3. [Color Palette](#color-palette)
4. [Typography](#typography)
5. [Component Library](#component-library)
6. [Page Templates](#page-templates)
7. [SEO Best Practices](#seo-best-practices)
8. [Responsive Design](#responsive-design)
9. [Accessibility](#accessibility)

---

## 🚀 Quick Start - Odoo 18 Implementation

### Step 1: Create a New Page in Odoo
1. Go to **Website → Site → Pages**
2. Click **New**
3. Name it "Home" and set URL to `/` or `/home`

### Step 2: Add HTML Code Block
1. Click **Edit** on your new page
2. Drag an **HTML/CSS/JS** block (or use "Code Editor" block)
3. Paste the entire content from `chaoshub_homepage.html`

### Step 3: Customize Links
Update these placeholder links to match your Odoo page structure:
- `/knowledge` → Your knowledge base URL
- `/contact` → Contact page URL
- `/about` → About page URL
- `/services` → Services page URL
- `/community` → Community/Forum URL

### Step 4: Configure Newsletter
Update the newsletter form action:
```html
<form class="newsletter-form" action="/website/form/subscribe" method="POST">
```

### Step 5: Add Social Media Links
Update footer social links with your actual profiles.

---

## 🎨 Design System Overview

This design system uses **CSS Custom Properties (Variables)** for consistency across all pages. All colors, spacing, typography, and components are centralized for easy maintenance.

### Core Philosophy
- **Consistency**: Reuse components and variables
- **Scalability**: Easy to add new pages
- **Performance**: Optimized for fast loading
- **Accessibility**: WCAG 2.1 AA compliant
- **SEO**: Semantic HTML and proper meta tags

---

## 🌈 Color Palette

### Primary Colors
```css
--color-primary: #6366f1        /* Indigo - Main brand color */
--color-primary-dark: #4f46e5   /* Darker indigo - Hover states */
--color-primary-light: #818cf8  /* Light indigo - Accents */
--color-secondary: #ec4899      /* Pink - Secondary actions */
--color-accent: #14b8a6         /* Teal - Highlights */
```

### Neutral Colors
```css
--color-dark: #0f172a           /* Dark slate - Primary text */
--color-dark-alt: #1e293b       /* Alternative dark - Backgrounds */
--color-gray: #64748b           /* Slate gray - Body text */
--color-gray-light: #cbd5e1     /* Light gray - Borders */
--color-gray-lighter: #f1f5f9   /* Very light gray - Backgrounds */
--color-white: #ffffff          /* Pure white */
```

### Gradients
```css
--gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)
--gradient-secondary: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)
--gradient-accent: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%)
--gradient-dark: linear-gradient(135deg, #0f172a 0%, #1e293b 100%)
```

### Usage Examples
```html
<!-- Primary button -->
<a href="#" class="btn btn-primary">Click Me</a>

<!-- Secondary button -->
<a href="#" class="btn btn-secondary">Learn More</a>

<!-- Text with gradient -->
<h2 class="text-gradient">Gradient Heading</h2>
```

---

## 📝 Typography

### Font Families
- **Headings**: Sora (Bold, Modern)
- **Body**: Inter (Clean, Readable)
- **Fallback**: System fonts for performance

### Font Sizes (Responsive)
```css
--text-xs: 0.75rem      /* 12px */
--text-sm: 0.875rem     /* 14px */
--text-base: 1rem       /* 16px */
--text-lg: 1.125rem     /* 18px */
--text-xl: 1.25rem      /* 20px */
--text-2xl: 1.5rem      /* 24px */
--text-3xl: 1.875rem    /* 30px */
--text-4xl: 2.25rem     /* 36px */
--text-5xl: 3rem        /* 48px */
--text-6xl: 3.75rem     /* 60px */
```

### Heading Hierarchy
```html
<h1>Main Page Title</h1>          <!-- Only one per page -->
<h2>Section Titles</h2>            <!-- Major sections -->
<h3>Subsection Titles</h3>         <!-- Cards, articles -->
<h4>Small Headings</h4>            <!-- Minor elements -->
```

---

## 🧩 Component Library

### 1. Buttons

#### Primary Button
```html
<a href="#" class="btn btn-primary">Primary Action</a>
```

#### Secondary Button
```html
<a href="#" class="btn btn-secondary">Secondary Action</a>
```

#### Large Button
```html
<a href="#" class="btn btn-primary btn-lg">Large Button</a>
```

---

### 2. Cards

#### Basic Card
```html
<div class="card">
    <div class="card-icon">📊</div>
    <h3 class="card-title">Card Title</h3>
    <p class="card-text">Card description goes here.</p>
</div>
```

#### Knowledge Card (with top border animation)
```html
<div class="card knowledge-card">
    <div class="card-icon">💡</div>
    <h3 class="card-title">Knowledge Topic</h3>
    <p class="card-text">Brief description of the topic.</p>
</div>
```

#### Article Card
```html
<article class="article-card">
    <div class="article-image">📚</div>
    <div class="article-content">
        <div class="article-meta">
            <span class="article-tag">Category</span>
            <span>5 min read</span>
        </div>
        <h3 class="article-title">Article Title</h3>
        <p class="article-excerpt">Brief excerpt of the article content...</p>
        <a href="/article-url" class="article-link">Read More →</a>
    </div>
</article>
```

---

### 3. Grid Layouts

#### 2 Column Grid
```html
<div class="grid grid-2">
    <div class="card">...</div>
    <div class="card">...</div>
</div>
```

#### 3 Column Grid
```html
<div class="grid grid-3">
    <div class="card">...</div>
    <div class="card">...</div>
    <div class="card">...</div>
</div>
```

#### 4 Column Grid
```html
<div class="grid grid-4">
    <div class="card">...</div>
    <div class="card">...</div>
    <div class="card">...</div>
    <div class="card">...</div>
</div>
```

---

### 4. Section Headers

```html
<div class="section-header">
    <span class="section-badge">Category Label</span>
    <h2 class="section-title">Section Title</h2>
    <p class="section-description">
        Brief description of what this section contains.
    </p>
</div>
```

---

### 5. CTA Banner

```html
<div class="cta-banner">
    <div class="cta-content">
        <h2>Call to Action Title</h2>
        <p>Compelling description encouraging user action.</p>
        <div class="cta-buttons">
            <a href="#" class="btn btn-primary btn-lg">Primary CTA</a>
            <a href="#" class="btn btn-secondary btn-lg">Secondary CTA</a>
        </div>
    </div>
</div>
```

---

### 6. Newsletter Form

```html
<div class="newsletter">
    <h3>Newsletter Title</h3>
    <p>Subscribe to receive updates.</p>
    <form class="newsletter-form" action="/subscribe" method="POST">
        <input
            type="email"
            class="newsletter-input"
            placeholder="Enter your email"
            required
            name="email"
        >
        <button type="submit" class="btn btn-primary">Subscribe</button>
    </form>
</div>
```

---

## 📄 Page Templates

### Template Structure
All pages should follow this consistent structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- SEO Meta Tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Page-specific description">
    <title>Page Title | ChaosHub.lk</title>

    <!-- Fonts & Styles (reuse from homepage) -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        /* Paste the entire CSS from homepage */
        /* OR link to external stylesheet */
    </style>
</head>
<body>
    <!-- Page content -->

    <!-- Reuse footer from homepage -->
</body>
</html>
```

---

### News/Blog Page Template

```html
<!-- Hero Section -->
<section class="hero" style="min-height: 60vh;">
    <div class="container">
        <div class="hero-content">
            <span class="hero-badge">Knowledge Hub</span>
            <h1>Latest News & Insights</h1>
            <p class="hero-subtext">
                Stay updated with the latest articles, guides, and industry insights.
            </p>
        </div>
    </div>
</section>

<!-- Articles Grid -->
<section class="section">
    <div class="container">
        <div class="grid grid-3">
            <!-- Repeat article cards -->
            <article class="article-card">
                <!-- Article content -->
            </article>
        </div>
    </div>
</section>
```

---

### Services Page Template

```html
<!-- Hero Section -->
<section class="hero" style="min-height: 60vh;">
    <div class="container">
        <div class="hero-content">
            <span class="hero-badge">Our Services</span>
            <h1>Services We Offer</h1>
            <p class="hero-subtext">
                Comprehensive business solutions to help you succeed.
            </p>
        </div>
    </div>
</section>

<!-- Services Grid -->
<section class="section">
    <div class="container">
        <div class="grid grid-3">
            <div class="card">
                <div class="card-icon">🎯</div>
                <h3 class="card-title">Service Name</h3>
                <p class="card-text">Service description.</p>
                <a href="#" class="btn btn-primary">Learn More</a>
            </div>
            <!-- Repeat for each service -->
        </div>
    </div>
</section>
```

---

### About Us Page Template

```html
<!-- Hero Section -->
<section class="hero" style="min-height: 60vh;">
    <div class="container">
        <div class="hero-content">
            <span class="hero-badge">About ChaosHub</span>
            <h1>Engineering Clarity from Chaos</h1>
            <p class="hero-subtext">
                Learn about our mission, vision, and values.
            </p>
        </div>
    </div>
</section>

<!-- About Content -->
<section class="section">
    <div class="container">
        <div class="about-grid">
            <div class="about-content">
                <h2>Our Story</h2>
                <p>Content about company history...</p>
            </div>
            <div class="about-visual">
                <div class="about-icon">🚀</div>
            </div>
        </div>
    </div>
</section>

<!-- Team/Values Section -->
<section class="section section-alt">
    <div class="container">
        <div class="section-header">
            <h2>Our Values</h2>
        </div>
        <div class="grid grid-3">
            <div class="card feature-card">
                <div class="feature-icon">✓</div>
                <h3 class="card-title">Value Name</h3>
                <p class="card-text">Value description.</p>
            </div>
            <!-- Repeat -->
        </div>
    </div>
</section>
```

---

### Contact Us Page Template

```html
<!-- Hero Section -->
<section class="hero" style="min-height: 60vh;">
    <div class="container">
        <div class="hero-content">
            <span class="hero-badge">Get In Touch</span>
            <h1>Contact Us</h1>
            <p class="hero-subtext">
                We'd love to hear from you. Send us a message.
            </p>
        </div>
    </div>
</section>

<!-- Contact Form Section -->
<section class="section">
    <div class="container">
        <div class="grid grid-2">
            <!-- Contact Information -->
            <div>
                <h2>Get in Touch</h2>
                <p>Contact information and details...</p>

                <div class="card">
                    <h4>📧 Email</h4>
                    <p>hello@chaoshub.lk</p>
                </div>

                <div class="card">
                    <h4>📱 Phone</h4>
                    <p>+94 XX XXX XXXX</p>
                </div>
            </div>

            <!-- Contact Form -->
            <div class="card">
                <form action="/website/form/contact" method="POST">
                    <div style="margin-bottom: 1rem;">
                        <label>Name</label>
                        <input type="text" class="newsletter-input" style="width: 100%;" required>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label>Email</label>
                        <input type="email" class="newsletter-input" style="width: 100%;" required>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label>Message</label>
                        <textarea class="newsletter-input" style="width: 100%; min-height: 150px;" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width: 100%;">Send Message</button>
                </form>
            </div>
        </div>
    </div>
</section>
```

---

### Help Page Template

```html
<!-- Hero Section -->
<section class="hero" style="min-height: 60vh;">
    <div class="container">
        <div class="hero-content">
            <span class="hero-badge">Support Center</span>
            <h1>How Can We Help?</h1>
            <p class="hero-subtext">
                Find answers to common questions and get support.
            </p>
        </div>
    </div>
</section>

<!-- FAQ Section -->
<section class="section">
    <div class="container">
        <div class="section-header">
            <h2>Frequently Asked Questions</h2>
        </div>

        <div style="max-width: 800px; margin: 0 auto;">
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>Question 1?</h3>
                <p>Answer to the question...</p>
            </div>

            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>Question 2?</h3>
                <p>Answer to the question...</p>
            </div>

            <!-- Repeat for more FAQs -->
        </div>
    </div>
</section>

<!-- Contact CTA -->
<section class="section section-alt">
    <div class="container">
        <div class="cta-banner">
            <div class="cta-content">
                <h2>Still Need Help?</h2>
                <p>Our team is here to assist you.</p>
                <a href="/contact" class="btn btn-primary btn-lg">Contact Support</a>
            </div>
        </div>
    </div>
</section>
```

---

## 🔍 SEO Best Practices

### Page-Specific Meta Tags
Every page should have unique meta tags:

```html
<head>
    <!-- Title: 50-60 characters -->
    <title>Page Title | ChaosHub.lk</title>

    <!-- Description: 150-160 characters -->
    <meta name="description" content="Unique page description">

    <!-- Keywords: 5-10 relevant terms -->
    <meta name="keywords" content="keyword1, keyword2, keyword3">

    <!-- Open Graph for Social Sharing -->
    <meta property="og:title" content="Page Title">
    <meta property="og:description" content="Page description">
    <meta property="og:image" content="https://chaoshub.lk/images/page-og.jpg">
    <meta property="og:url" content="https://chaoshub.lk/page-url">
</head>
```

### Semantic HTML Structure
```html
<article>  <!-- For blog posts, articles -->
<section>  <!-- For distinct sections -->
<nav>      <!-- For navigation menus -->
<header>   <!-- For page headers -->
<footer>   <!-- For page footers -->
<aside>    <!-- For sidebars, related content -->
```

### Heading Hierarchy
- Only one `<h1>` per page (main title)
- Use `<h2>` for major sections
- Use `<h3>` for subsections
- Maintain logical order (don't skip levels)

### Image Optimization
```html
<img
    src="image.jpg"
    alt="Descriptive text for accessibility and SEO"
    width="800"
    height="600"
    loading="lazy"
>
```

### Internal Linking
Link to relevant pages within your site:
```html
<p>
    Learn more about <a href="/services">our services</a> or
    <a href="/contact">get in touch</a>.
</p>
```

---

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile: Default styles (mobile-first) */

/* Tablet */
@media (max-width: 768px) {
    /* Tablet styles */
}

/* Small Mobile */
@media (max-width: 480px) {
    /* Small mobile styles */
}
```

### Mobile-Friendly Checklist
- ✅ Touch-friendly buttons (min 44px height)
- ✅ Readable text (min 16px font size)
- ✅ No horizontal scrolling
- ✅ Stacked layouts on mobile
- ✅ Fast loading (< 3 seconds)

---

## ♿ Accessibility

### ARIA Labels
```html
<button aria-label="Close menu">×</button>
<nav aria-label="Main navigation">...</nav>
<input type="email" aria-label="Email address" placeholder="Email">
```

### Keyboard Navigation
All interactive elements should be keyboard accessible:
```css
.btn:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}
```

### Color Contrast
- Text on background: minimum 4.5:1 ratio
- Large text (18px+): minimum 3:1 ratio
- Use tools like WebAIM Contrast Checker

### Alt Text for Images
```html
<img src="chart.png" alt="Sales growth chart showing 50% increase">
```

---

## 🛠️ Maintenance & Updates

### Updating Colors Site-Wide
Change CSS variables at the top of the stylesheet:
```css
:root {
    --color-primary: #NEW-COLOR;
}
```

### Adding New Components
1. Follow existing naming conventions
2. Use CSS variables for colors/spacing
3. Ensure responsive design
4. Test on mobile devices
5. Document in this guide

### Performance Optimization
- Minimize CSS (remove unused styles)
- Optimize images (WebP format, compress)
- Use lazy loading for images
- Enable browser caching
- Consider CDN for fonts

---

## 📊 Performance Metrics

### Target Metrics
- **Page Load Time**: < 3 seconds
- **First Contentful Paint**: < 1.5 seconds
- **Largest Contentful Paint**: < 2.5 seconds
- **Time to Interactive**: < 3.5 seconds
- **Cumulative Layout Shift**: < 0.1

### Testing Tools
- Google PageSpeed Insights
- GTmetrix
- WebPageTest
- Lighthouse (Chrome DevTools)

---

## 🎯 Next Steps

1. **Implement Homepage**: Copy the HTML to Odoo
2. **Create Other Pages**: Use templates provided above
3. **Customize Content**: Replace placeholder text with actual content
4. **Test Thoroughly**: Check all devices and browsers
5. **Optimize SEO**: Add unique meta tags for each page
6. **Monitor Performance**: Use analytics and testing tools

---

## 📞 Support

For questions or assistance:
- Email: dev@chaoshub.lk
- Documentation: This file
- Odoo Documentation: https://www.odoo.com/documentation/18.0/

---

**Last Updated**: December 2025
**Version**: 1.0.0
**Created for**: Odoo 18 Community Edition