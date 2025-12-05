#!/usr/bin/env python3
"""
Extract image URLs from a backup HTML file and save them to image_urls_clean.txt
Works with images from any source (CDN, external hosting, etc.)
Supports: .png, .jpg, .jpeg, .gif, .webp, .svg
"""
import re
from pathlib import Path
import sys

# Get file from command line or prompt
if len(sys.argv) > 1:
    backup_file = sys.argv[1]
else:
    backup_file = input("Enter backup file name (e.g., newsletter-8-backup.html): ").strip()

if not Path(backup_file).exists():
    print(f"Error: {backup_file} not found!")
    sys.exit(1)

urls = set()

with open(backup_file, 'r', encoding='utf-8') as f:
    content = f.read()
    # Extract any HTTP/HTTPS image URLs (not just stripocdn.email)
    # Pattern matches: http:// or https:// followed by domain and path ending with image extensions
    matches = re.findall(r'https?://[^\s\"\'\>\)]+\.(?:png|jpg|jpeg|gif|webp|svg)', content, re.IGNORECASE)
    for match in matches:
        # Remove trailing characters that might be part of HTML attributes
        url = match.split(')')[0].split('"')[0].split("'")[0].split('>')[0].split(' ')[0]
        if url.startswith(('http://', 'https://')) and url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
            urls.add(url)

# Write cleaned URLs
output_file = 'image_urls_clean.txt'
with open(output_file, 'w') as f:
    for url in sorted(urls):
        f.write(url + '\n')

print(f'✓ Found {len(urls)} unique image URLs')
print(f'  Saved to {output_file}')

