# Email Template Sections

This folder contains modular, reusable sections for email templates. Each section is standalone and can be mixed and matched to create custom email templates.

## Folder Structure

- **headers/** - Preheader and header sections with logos and navigation
- **heroes/** - Hero sections with background images and call-to-action content
- **products/** - Product grid sections and product showcases
- **cta/** - Call-to-action button sections
- **buttons/** - Standalone button components
- **testimonials/** - Customer testimonial sections
- **blog/** - Blog post showcase sections
- **footer/** - Footer sections with social links, contact info, and unsubscribe
- **misc/** - Miscellaneous sections (features, categories, brands, etc.)

## Usage

Each section file contains HTML table rows (`<tr>`) that can be directly included in email templates. Simply copy the content of a section file and paste it into your email template's main table structure.

## Preview System

### Viewing Sections Overview

Open `overview.html` in your browser to see all available sections with live previews.

**Important:** The preview system requires a local web server to work properly due to browser security restrictions. 

### Running a Local Server

To view the overview with working previews, start a local server:

```bash
# Python 3
python3 -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (if you have http-server installed)
npx http-server -p 8000

# PHP
php -S localhost:8000
```

Then open: `http://localhost:8000/sections/overview.html`

### Without a Server

If you open `overview.html` directly (file:// protocol), the previews won't load due to CORS restrictions. However, you can still:
- View the section list
- Click "View Section" to see the raw HTML
- Download sections directly

## Example

```html
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" class="email-container">
    <!-- Include preheader -->
    <!--#include virtual="sections/headers/preheader-avora-1.html" -->
    
    <!-- Include header -->
    <!--#include virtual="sections/headers/header-avora-1.html" -->
    
    <!-- Include hero -->
    <!--#include virtual="sections/heroes/hero-avora-fall-sale.html" -->
    
    <!-- Include products -->
    <!--#include virtual="sections/products/product-grid-3-column.html" -->
    
    <!-- Include footer -->
    <!--#include virtual="sections/footer/footer-avora-complete.html" -->
</table>
```

Note: Server-side includes (SSI) may not work in all email clients. For production use, manually copy the section content into your templates or use a build process to combine sections.
