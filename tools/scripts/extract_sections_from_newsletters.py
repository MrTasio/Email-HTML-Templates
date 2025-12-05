#!/usr/bin/env python3
"""
Script to extract sections from newsletter-5.html, newsletter-6.html, and newsletter-7.html
and create standalone section files with their own background colors.
"""

import re
from pathlib import Path
from html.parser import HTMLParser

def extract_bgcolor(html_content):
    """Extract background color from bgcolor attribute or style."""
    # Try bgcolor attribute first
    bgcolor_match = re.search(r'bgcolor=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if bgcolor_match:
        return bgcolor_match.group(1)
    
    # Try background-color in style
    bg_match = re.search(r'background-color:\s*([^;\)]+)', html_content, re.IGNORECASE)
    if bg_match:
        return bg_match.group(1).strip()
    
    # Try background in style
    bg_match = re.search(r'background:\s*([^;\)]+)', html_content, re.IGNORECASE)
    if bg_match:
        bg = bg_match.group(1).strip()
        # If it's a color (not an image URL), return it
        if not bg.startswith('url') and not bg.startswith('http'):
            return bg
    
    return None

def extract_sections_from_newsletter(newsletter_path, newsletter_num):
    """Extract sections from a newsletter file."""
    with open(newsletter_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = []
    
    # Find all table sections with bgcolor or background-color
    # Look for patterns like: <table ... bgcolor="..." or <table ... style="...background-color:..."
    # Each section is typically wrapped in a table with class="cp" or class="co" or similar
    
    # Split by major table sections
    # Pattern: table with bgcolor or background-color, followed by content until next major table
    table_pattern = r'<table[^>]*(?:bgcolor=["\']([^"\']+)["\']|style=["\'][^"\']*background-color:\s*([^;\)]+)[^"\']*["\'])[^>]*>.*?</table>'
    
    # More specific: find tables that are section containers
    # These are usually: <table class="cp" or <table class="co" with bgcolor
    section_tables = re.finditer(
        r'<table[^>]*class=["\'](?:cp|co|cb|cc)[^"\']*["\'][^>]*(?:bgcolor=["\']([^"\']+)["\']|style=["\'][^"\']*background-color:\s*([^;\)]+)[^"\']*["\'])[^>]*>.*?</table>',
        content,
        re.DOTALL | re.IGNORECASE
    )
    
    # Alternative: find sections by looking for table rows that contain distinct content
    # We'll use a simpler approach: find all <tr> sections that are children of main content tables
    
    # Extract sections manually based on known patterns
    # For newsletter-5: header (white), hero (white), products (white), promo (cdc9c4), footer (dark)
    # For newsletter-6: header (white), hero (white), calendar (dark #0F1011), movie detail (dark), footer
    # For newsletter-7: header (green #09664e), hero (green), event details (green), footer
    
    return sections

def create_standalone_section(content, bgcolor, section_name, category):
    """Create a standalone HTML file for a section with its background color."""
    
    # Default background if none found
    if not bgcolor:
        bgcolor = '#ffffff'
    
    # Clean up bgcolor value
    bgcolor = bgcolor.strip().strip('"\'')
    
    # Extract just the table rows/content (remove outer wrapper tables)
    # Find the main content <tr> tags
    tr_content = re.search(r'<tr[^>]*>.*?</tr>', content, re.DOTALL)
    if tr_content:
        section_content = tr_content.group(0)
    else:
        # If no <tr> found, use the content as-is but wrap it
        section_content = content
    
    # Update image paths to be root-relative
    section_content = re.sub(r'src=["\']assets/', r'src="/assets/', section_content)
    section_content = re.sub(r'src=["\']([^"\']*assets/)', r'src="/\1', section_content)
    
    # Constrain width attributes
    section_content = re.sub(r'width="(\d+)"', lambda m: f'width="{min(int(m.group(1)), 600)}"' if int(m.group(1)) > 600 else m.group(0), section_content)
    
    # Create standalone HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{section_name.replace('-', ' ').title()}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }}
        .email-container {{
            max-width: 600px;
            width: 100%;
            margin: 0 auto;
            background: {bgcolor};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .email-container table {{
            max-width: 600px !important;
            width: 100% !important;
        }}
        table {{
            width: 100% !important;
            max-width: 600px !important;
            border-collapse: collapse;
        }}
        table[width] {{
            max-width: 600px !important;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            border: 0;
        }}
        a {{
            color: inherit;
            text-decoration: none;
        }}
        table[role="presentation"] {{
            border-collapse: collapse;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
            max-width: 600px !important;
        }}
        td {{
            padding: 0;
        }}
        .esdev-mso-table {{
            max-width: 600px !important;
            width: 100% !important;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; width: 100%; background-color: {bgcolor};">
{section_content}
        </table>
    </div>
</body>
</html>'''
    
    return html

def main():
    """Main extraction function."""
    base_dir = Path(__file__).parent.parent.parent
    sections_dir = base_dir / 'sections'
    
    # Define sections to extract from each newsletter
    newsletter_sections = {
        5: [
            {
                'name': 'header-travel-logo',
                'category': 'headers',
                'start_marker': '<!-- Header with Logo -->',
                'bgcolor': '#ffffff'
            },
            {
                'name': 'hero-travel-banner',
                'category': 'heroes',
                'start_marker': 'hero',
                'bgcolor': '#ffffff'
            },
            {
                'name': 'product-showcase-3-column-travel',
                'category': 'products',
                'start_marker': 'Product Showcase',
                'bgcolor': '#ffffff'
            },
            {
                'name': 'promo-box-travel',
                'category': 'cta',
                'start_marker': 'Promotional Box',
                'bgcolor': '#CDC9C4'
            },
            {
                'name': 'blog-travel-2-column',
                'category': 'blog',
                'start_marker': 'Blog',
                'bgcolor': '#ffffff'
            },
            {
                'name': 'footer-travel-contact',
                'category': 'footer',
                'start_marker': 'Footer with Contact',
                'bgcolor': '#333333'
            },
            {
                'name': 'footer-travel-unsubscribe',
                'category': 'footer',
                'start_marker': 'Footer with Unsubscribe',
                'bgcolor': '#333333'
            }
        ],
        6: [
            {
                'name': 'header-movie-logo',
                'category': 'headers',
                'start_marker': 'header',
                'bgcolor': '#ffffff'
            },
            {
                'name': 'hero-movie-advent',
                'category': 'heroes',
                'start_marker': 'Hero Movie Advent',
                'bgcolor': '#ffffff'
            },
            {
                'name': 'product-grid-movie-calendar',
                'category': 'products',
                'start_marker': 'Movie Calendar',
                'bgcolor': '#0F1011'
            },
            {
                'name': 'movie-detail-section',
                'category': 'misc',
                'start_marker': 'Movie Detail',
                'bgcolor': '#0F1011'
            }
        ],
        7: [
            {
                'name': 'header-party-logo',
                'category': 'headers',
                'start_marker': 'header',
                'bgcolor': '#09664e'
            },
            {
                'name': 'hero-party-banner',
                'category': 'heroes',
                'start_marker': 'Hero Party',
                'bgcolor': '#09664e'
            },
            {
                'name': 'event-details-section',
                'category': 'misc',
                'start_marker': 'Event Details',
                'bgcolor': '#00533E'
            }
        ]
    }
    
    for newsletter_num in [5, 6, 7]:
        newsletter_path = base_dir / f'newsletter-{newsletter_num}.html'
        
        if not newsletter_path.exists():
            print(f"Warning: {newsletter_path} not found, skipping...")
            continue
        
        print(f"\nProcessing newsletter-{newsletter_num}.html...")
        
        with open(newsletter_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract sections based on markers
        for section_def in newsletter_sections.get(newsletter_num, []):
            section_name = section_def['name']
            category = section_def['category']
            bgcolor = section_def.get('bgcolor', '#ffffff')
            start_marker = section_def.get('start_marker', '')
            
            # Find section in content
            # Look for the section by finding table rows that contain the marker
            # We'll use a simpler approach: read existing section files and update them
            
            # For now, let's read the existing section files and update their background colors
            section_file = sections_dir / category / f'{section_name}.html'
            
            if section_file.exists():
                print(f"  Updating {section_name}...")
                
                # Read existing section
                with open(section_file, 'r', encoding='utf-8') as f:
                    section_content = f.read()
                
                # Extract the actual section content (table rows)
                # Remove the wrapper HTML if it exists
                if '<!DOCTYPE' in section_content:
                    # Extract just the table rows
                    tr_match = re.search(r'<tr[^>]*>.*?</tr>', section_content, re.DOTALL)
                    if tr_match:
                        section_rows = tr_match.group(0)
                    else:
                        # Try to find content between <table> tags
                        table_match = re.search(r'<table[^>]*>(.*?)</table>', section_content, re.DOTALL)
                        if table_match:
                            section_rows = table_match.group(1)
                        else:
                            section_rows = section_content
                else:
                    section_rows = section_content
                
                # Create new standalone section with background color
                new_content = create_standalone_section(section_rows, bgcolor, section_name, category)
                
                # Write updated section
                with open(section_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"    ✓ Updated with background color: {bgcolor}")
            else:
                print(f"  Warning: {section_file} not found, skipping...")
    
    print("\nDone! All sections updated with their background colors.")

if __name__ == '__main__':
    main()

