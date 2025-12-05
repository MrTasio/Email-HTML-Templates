#!/usr/bin/env python3
"""
Script to wrap section HTML files in complete email template structure with max-width constraints.
"""

import os
import re
from pathlib import Path

def wrap_section_file(file_path):
    """Wrap a section file in complete HTML email template structure."""
    
    # Read the current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Check if already wrapped (has DOCTYPE)
    if content.startswith('<!DOCTYPE'):
        print(f"  Skipping {file_path.name} - already wrapped")
        return False
    
    # Constrain width attributes that exceed 600px
    content = re.sub(r'width="(\d+)"', lambda m: f'width="{min(int(m.group(1)), 600)}"' if int(m.group(1)) > 600 else m.group(0), content)
    content = re.sub(r'width:(\d+)px', lambda m: f'width:{min(int(m.group(1)), 600)}px' if int(m.group(1)) > 600 else m.group(0), content)
    
    # Wrap in complete HTML structure
    wrapped_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{file_path.stem.replace('-', ' ').title()}</title>
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
            background: #ffffff;
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
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; width: 100%; background-color: #ffffff;">
{content}
        </table>
    </div>
</body>
</html>'''
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(wrapped_content)
    
    print(f"  Wrapped {file_path.name}")
    return True

def main():
    """Main function to process all section files."""
    sections_dir = Path(__file__).parent.parent.parent / 'sections'
    
    if not sections_dir.exists():
        print(f"Error: Sections directory not found at {sections_dir}")
        return
    
    # Find all HTML files in sections directory
    html_files = list(sections_dir.rglob('*.html'))
    
    if not html_files:
        print("No HTML files found in sections directory")
        return
    
    print(f"Found {len(html_files)} HTML files")
    print("Wrapping sections in email template structure...\n")
    
    wrapped_count = 0
    for file_path in html_files:
        if wrap_section_file(file_path):
            wrapped_count += 1
    
    print(f"\nDone! Wrapped {wrapped_count} files.")

if __name__ == '__main__':
    main()

