#!/usr/bin/env python3
"""
Download images from URLs listed in image_urls_clean.txt
and save them to the assets/ folder with proper organization.
"""
import os
import re
import urllib.request
import ssl
from urllib.parse import urlparse
from pathlib import Path
import sys

# Create unverified SSL context (for downloading)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create assets directory
assets_dir = Path('assets')
assets_dir.mkdir(exist_ok=True)

# Check if URL file exists
url_file = 'image_urls_clean.txt'
if not Path(url_file).exists():
    print(f"Error: {url_file} not found!")
    print("Please create it first by extracting URLs from your backup file.")
    sys.exit(1)

# Read URLs from file
urls = []
with open(url_file, 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

if not urls:
    print(f"No URLs found in {url_file}")
    sys.exit(1)

print(f"Downloading {len(urls)} images...")

# Create a mapping of original URLs to local paths
url_to_local = {}
errors = []

for url in urls:
    try:
        # Parse URL to get path components
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        
        # Extract filename
        filename = path_parts[-1]
        
        # Create a safe directory structure
        if len(path_parts) > 1:
            subdir = path_parts[-2] if path_parts[-2] != 'images' else path_parts[-3] if len(path_parts) > 2 else 'images'
        else:
            subdir = 'images'
        
        # Sanitize subdir name
        subdir = re.sub(r'[^a-zA-Z0-9_-]', '_', subdir)
        subdir_dir = assets_dir / subdir
        subdir_dir.mkdir(exist_ok=True)
        
        # Local file path
        local_path = subdir_dir / filename
        local_url = f"assets/{subdir}/{filename}"
        
        # Download if not exists
        if not local_path.exists():
            print(f"Downloading: {filename}")
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ssl_context) as response:
                with open(local_path, 'wb') as out_file:
                    out_file.write(response.read())
        else:
            print(f"Skipping (exists): {filename}")
        
        url_to_local[url] = local_url
        
    except Exception as e:
        error_msg = f"Error downloading {url}: {e}"
        print(error_msg)
        errors.append(error_msg)

# Save mapping for later use
mapping_file = 'url_mapping.txt'
with open(mapping_file, 'w') as f:
    for orig_url, local_url in sorted(url_to_local.items()):
        f.write(f"{orig_url}|{local_url}\n")

print(f"\nDownloaded {len(url_to_local)} images successfully!")
if errors:
    print(f"\n{len(errors)} errors occurred:")
    for error in errors:
        print(f"  - {error}")
print(f"Mapping saved to {mapping_file}")

