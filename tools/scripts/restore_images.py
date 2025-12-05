#!/usr/bin/env python3
"""
Restore images in newsletter file from backup file.
Replaces src="#" placeholders with actual image URLs from backup.
Works with images from any source (CDN, external hosting, etc.)
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

# Get files from command line or prompt
if len(sys.argv) >= 3:
    backup_file = sys.argv[1]
    current_file = sys.argv[2]
else:
    backup_file = input("Enter backup file name (e.g., newsletter-8-backup.html): ").strip()
    current_file = input("Enter current file name (e.g., newsletter-8.html): ").strip()

if not Path(backup_file).exists():
    print(f"Error: {backup_file} not found!")
    sys.exit(1)

if not Path(current_file).exists():
    print(f"Error: {current_file} not found!")
    sys.exit(1)

# Read backup file
with open(backup_file, 'r', encoding='utf-8') as f:
    backup_content = f.read()

# Read current file
with open(current_file, 'r', encoding='utf-8') as f:
    current_content = f.read()

# Extract all image URLs from backup in order (any HTTP/HTTPS URL)
img_urls = []
for match in re.finditer(r'src="(https?://[^"]+\.(?:png|jpg|jpeg|gif|webp|svg))"', backup_content, re.IGNORECASE):
    img_urls.append(match.group(1))

# Find all img tags with src="#" in current file
img_tags_with_hash = []
for match in re.finditer(r'(<img[^>]+src="#"[^>]*>)', current_content):
    img_tags_with_hash.append(match.group(1))

if not img_tags_with_hash:
    print("No images with src='#' found. File may already be restored.")
    sys.exit(0)

# Replace each src="#" with corresponding URL from backup
replacements = 0
for i, img_tag in enumerate(img_tags_with_hash):
    if i < len(img_urls):
        orig_url = img_urls[i]
        if orig_url in url_mapping:
            local_url = url_mapping[orig_url]
            # Replace src="#" with local URL
            new_tag = img_tag.replace('src="#"', f'src="{local_url}"')
            current_content = current_content.replace(img_tag, new_tag, 1)
            replacements += 1
            print(f"  Restored image {i+1}: {Path(local_url).name}")

# Also handle background-image URLs (any HTTP/HTTPS URL)
bg_urls = []
for match in re.finditer(r'background-image:\s*url\((https?://[^)]+\.(?:png|jpg|jpeg|gif|webp|svg))\)', backup_content, re.IGNORECASE):
    bg_urls.append(match.group(1))

bg_replacements = 0
for bg_url in bg_urls:
    if bg_url in url_mapping:
        local_url = url_mapping[bg_url]
        pattern = r'background-image:\s*url\(#\)'
        replacement = f'background-image: url({local_url})'
        if re.search(pattern, current_content):
            current_content = re.sub(pattern, replacement, current_content, count=1)
            bg_replacements += 1

# Also handle background="..." attributes (any HTTP/HTTPS URL)
bg_attrs = []
for match in re.finditer(r'background="(https?://[^"]+\.(?:png|jpg|jpeg|gif|webp|svg))"', backup_content, re.IGNORECASE):
    bg_attrs.append(match.group(1))

for bg_url in bg_attrs:
    if bg_url in url_mapping:
        local_url = url_mapping[bg_url]
        # Replace background="#" with local URL
        current_content = current_content.replace('background="#"', f'background="{local_url}"')
        bg_replacements += 1

# Write updated content
if replacements > 0 or bg_replacements > 0:
    with open(current_file, 'w', encoding='utf-8') as f:
        f.write(current_content)
    print(f"\n✓ Updated {current_file}: {replacements} images, {bg_replacements} backgrounds")
else:
    print("\nNo replacements made. Check that backup file contains matching image URLs.")

