# Standard Operating Procedure: Adding a New Newsletter Template

This SOP outlines the process for adding a new newsletter template file and ensuring all images are properly downloaded and referenced locally.

## Prerequisites

- Python 3.x installed
- New newsletter HTML file (e.g., `newsletter-8.html`)
- Backup file with original image URLs (recommended: `newsletter-8-backup.html`)

## Step-by-Step Process

### Step 1: Prepare Your Files

1. **Create your newsletter file** in the project root (e.g., `newsletter-8.html`)
2. **Keep a backup** with original image URLs in the `tools/` folder (e.g., `tools/newsletter-8-backup.html`)
   - This backup should contain the original HTML with all image URLs intact (from any source: CDN, external hosting, etc.)
   - This is crucial for restoring images if they get replaced with `#`

### Step 2: Extract Image URLs

**Option A: Use the provided script (Recommended)**
```bash
python3 tools/scripts/extract_urls.py tools/newsletter-8-backup.html
```

**Option B: Manual extraction**
Create a script or use the following Python command to extract all image URLs from your backup file (works with any image source):

```python
import re

backup_file = 'newsletter-8-backup.html'
urls = set()

with open(backup_file, 'r') as f:
    content = f.read()
    # Extract any HTTP/HTTPS image URLs (works with any domain)
    matches = re.findall(r'https?://[^\s\"\'\>\)]+\.(?:png|jpg|jpeg|gif|webp|svg)', content, re.IGNORECASE)
    for match in matches:
        # Remove trailing characters that might be part of HTML attributes
        url = match.split(')')[0].split('"')[0].split("'")[0].split('>')[0].split(' ')[0]
        if url.startswith(('http://', 'https://')):
            urls.add(url)

# Write cleaned URLs
with open('image_urls_clean.txt', 'w') as f:
    for url in sorted(urls):
        f.write(url + '\n')

print(f'Found {len(urls)} unique image URLs')
```

### Step 3: Download Images

**Option A: Use the provided script (Recommended)**
```bash
python3 tools/scripts/download_images.py
```

**Option B: Manual script**
Use the provided `scripts/download_images.py` script (or create it using the template below):

```python
#!/usr/bin/env python3
import os
import re
import urllib.request
import ssl
from urllib.parse import urlparse
from pathlib import Path

# Create unverified SSL context (for downloading)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create assets directory
assets_dir = Path('assets')
assets_dir.mkdir(exist_ok=True)

# Read URLs from file
urls = []
with open('image_urls_clean.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Downloading {len(urls)} images...")

# Create a mapping of original URLs to local paths
url_to_local = {}

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
        print(f"Error downloading {url}: {e}")

# Save mapping for later use
with open('url_mapping.txt', 'w') as f:
    for orig_url, local_url in sorted(url_to_local.items()):
        f.write(f"{orig_url}|{local_url}\n")

print(f"\nDownloaded {len(url_to_local)} images successfully!")
print("Mapping saved to url_mapping.txt")
```

### Step 4: Update HTML File with Local Image Paths

**Option A: Use the provided script (Recommended)**
```bash
python3 tools/scripts/update_image_paths.py newsletter-8.html
```

**Option B: Manual script**
Create and run a script to replace remote URLs with local paths:

```python
#!/usr/bin/env python3
import re

# Load URL mapping
url_mapping = {}
with open('url_mapping.txt', 'r') as f:
    for line in f:
        if '|' in line:
            orig_url, local_url = line.strip().split('|', 1)
            url_mapping[orig_url] = local_url

# File to update
newsletter_file = 'newsletter-8.html'

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
        replacements += content.count(orig_url)
        content = content.replace(orig_url, local_url)

# Write updated content
if content != original_content:
    with open(newsletter_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {newsletter_file} ({replacements} replacements)")
else:
    print("No changes needed")
```

### Step 5: Restore Images if They Were Replaced with `#`

If your newsletter file has `src="#"` placeholders:

**Option A: Use the provided script (Recommended)**
```bash
python3 tools/scripts/restore_images.py tools/newsletter-8-backup.html newsletter-8.html
```

**Option B: Manual script**
Use this script to restore them from the backup:

```python
#!/usr/bin/env python3
import re
from pathlib import Path

# Load URL mapping
url_mapping = {}
with open('url_mapping.txt', 'r') as f:
    for line in f:
        if '|' in line:
            orig_url, local_url = line.strip().split('|', 1)
            url_mapping[orig_url] = local_url

backup_file = 'newsletter-8-backup.html'
current_file = 'newsletter-8.html'

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

# Write updated content
if replacements > 0 or bg_replacements > 0:
    with open(current_file, 'w', encoding='utf-8') as f:
        f.write(current_content)
    print(f"  Updated {current_file}: {replacements} images, {bg_replacements} backgrounds")
```

### Step 6: Verify Images Are Working

1. **Check for remaining `src="#"` placeholders:**
   ```bash
   grep -c 'src="#"' newsletter-8.html
   ```
   Should return `0` if all images are restored.

2. **Check that local paths exist:**
   ```bash
   grep -o 'assets/[^"]*' newsletter-8.html | sort -u | while read path; do
       if [ ! -f "$path" ]; then
           echo "Missing: $path"
       fi
   done
   ```

3. **Open the file in a browser** to visually verify all images load correctly.

### Step 7: Extract Sections (Optional)

If you want to extract sections from your newsletter:

1. Identify distinct sections in your HTML (headers, heroes, products, CTAs, footers, etc.)
2. Copy each section's HTML into a new file in the appropriate `sections/` subdirectory
3. Update image paths in section files to use relative paths from the sections directory
4. Add the section to `sections/overview.html` if you want it in the sections library

### Step 8: Clean Up Temporary Files

After completing the process, you can remove temporary files:

```bash
rm -f tools/image_urls_clean.txt tools/url_mapping.txt
```

**Note:** 
- Keep your backup file (`tools/newsletter-8-backup.html`) for future reference!
- The scripts in the `tools/scripts/` folder are reusable - keep them for future newsletters

## Quick Reference: One-Line Commands

### Extract URLs (works with any image source)
```bash
python3 -c "import re; urls=set(); content=open('tools/newsletter-8-backup.html').read(); [urls.add(m.split(')')[0].split('\"')[0].split(' ')[0]) for m in re.findall(r'https?://[^\s\"\'\>\)]+\.(?:png|jpg|jpeg|gif|webp|svg)', content, re.I) if m.startswith(('http://','https://'))]; open('tools/image_urls_clean.txt','w').write('\n'.join(sorted(urls))); print(f'Found {len(urls)} URLs')"
```

### Count images in file
```bash
grep -o 'src="[^"]*"' newsletter-8.html | wc -l
```

### Check for missing images
```bash
grep -o 'assets/[^"]*' newsletter-8.html | sort -u | xargs -I {} sh -c '[ -f "{}" ] || echo "Missing: {}"'
```

## Troubleshooting

### Images not downloading
- Check your internet connection
- Verify the URLs are accessible
- Check SSL certificate issues (the script handles this automatically)

### Images not restoring
- Ensure backup file has original URLs (from any source)
- Check that image order matches between backup and current file
- Manually match images by alt text or title attributes
- Verify URLs are valid HTTP/HTTPS links ending with image extensions (.png, .jpg, .gif, etc.)

### Path issues
- Ensure `assets/` folder exists
- Check file permissions
- Verify relative paths are correct

## Notes

- Always keep backup files with original URLs (works with images from any source: CDNs, external hosting, etc.)
- Images are organized by their source directory in `assets/`
- The mapping file (`url_mapping.txt`) can be reused for multiple files
- Section files should use the same image paths as their parent templates
- Scripts support images from any domain (not just stripocdn.email) - any HTTP/HTTPS URL ending with image extensions (.png, .jpg, .jpeg, .gif, .webp, .svg)

