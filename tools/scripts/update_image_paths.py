#!/usr/bin/env python3
"""
Update HTML file to replace remote image URLs with local asset paths.
"""
import re
from pathlib import Path
import sys

# Load URL mapping
mapping_file = 'url_mapping.txt'
if not Path(mapping_file).exists():
    print(f"Error: {mapping_file} not found!")
    print("Please run download_images.py first to create the mapping.")
    sys.exit(1)

url_mapping = {}
with open(mapping_file, 'r') as f:
    for line in f:
        if '|' in line:
            orig_url, local_url = line.strip().split('|', 1)
            url_mapping[orig_url] = local_url

if not url_mapping:
    print("No URL mappings found!")
    sys.exit(1)

# Get file to update from command line or use default
if len(sys.argv) > 1:
    newsletter_file = sys.argv[1]
else:
    newsletter_file = input("Enter newsletter file name (e.g., newsletter-8.html): ").strip()

if not Path(newsletter_file).exists():
    print(f"Error: {newsletter_file} not found!")
    sys.exit(1)

# Read current file
with open(newsletter_file, 'r', encoding='utf-8') as f:
    content = f.read()

original_content = content
replacements = 0

# Replace all URLs
for orig_url, local_url in url_mapping.items():
    # Replace in src attributes
    content = content.replace(f'src="{orig_url}"', f'src="{local_url}"')
    content = content.replace(f"src='{orig_url}'", f"src='{local_url}'")
    
    # Replace in background-image URLs
    content = content.replace(f'url({orig_url})', f'url({local_url})')
    content = content.replace(f"url('{orig_url}')", f"url('{local_url}')")
    content = content.replace(f'url("{orig_url}")', f'url("{local_url}")')
    
    # Replace in background attributes
    content = content.replace(f'background="{orig_url}"', f'background="{local_url}"')
    content = content.replace(f"background='{orig_url}'", f"background='{local_url}'")
    
    if orig_url in content:
        count = content.count(orig_url)
        content = content.replace(orig_url, local_url)
        replacements += count

# Write updated content
if content != original_content:
    with open(newsletter_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated: {newsletter_file}")
    print(f"  {replacements} URL replacements made")
else:
    print("No changes needed - file already uses local paths or no matching URLs found")

