# Newsletter Setup Scripts

These scripts automate the process of downloading images and updating newsletter HTML files.

## Quick Start

### 1. Extract Image URLs
```bash
python3 tools/scripts/extract_urls.py tools/newsletter-8-backup.html
```
This creates `tools/image_urls_clean.txt` with all image URLs from your backup file.

### 2. Download Images
```bash
python3 tools/scripts/download_images.py
```
Downloads all images from `tools/image_urls_clean.txt` to the `assets/` folder and creates `tools/url_mapping.txt`.

### 3. Update Image Paths
```bash
python3 tools/scripts/update_image_paths.py newsletter-8.html
```
Replaces remote URLs with local asset paths in your newsletter file.

### 4. Restore Images (if needed)
If your newsletter file has `src="#"` placeholders:
```bash
python3 tools/scripts/restore_images.py tools/newsletter-8-backup.html newsletter-8.html
```
Restores images from backup file using the URL mapping.

## Script Details

### `extract_urls.py`
- **Purpose**: Extract image URLs from backup HTML file
- **Input**: Backup HTML file (e.g., `newsletter-8-backup.html`)
- **Output**: `image_urls_clean.txt` (list of image URLs)

### `download_images.py`
- **Purpose**: Download images and organize them in `assets/` folder
- **Input**: `image_urls_clean.txt`
- **Output**: 
  - Images in `assets/` folder (organized by source directory)
  - `url_mapping.txt` (mapping of original URLs to local paths)

### `update_image_paths.py`
- **Purpose**: Replace remote image URLs with local paths
- **Input**: Newsletter HTML file (e.g., `newsletter-8.html`)
- **Output**: Updated HTML file with local image paths

### `restore_images.py`
- **Purpose**: Restore images that were replaced with `#`
- **Input**: 
  - Backup HTML file (with original URLs)
  - Current HTML file (with `src="#"` placeholders)
- **Output**: Updated HTML file with restored image paths

## Example Workflow

```bash
# Step 1: Extract URLs from backup
python3 tools/scripts/extract_urls.py tools/newsletter-8-backup.html

# Step 2: Download all images
python3 tools/scripts/download_images.py

# Step 3: Update your newsletter file
python3 tools/scripts/update_image_paths.py newsletter-8.html

# Step 4: If images were replaced with #, restore them
python3 tools/scripts/restore_images.py tools/newsletter-8-backup.html newsletter-8.html

# Step 5: Verify
grep -c 'src="#"' newsletter-8.html  # Should return 0
```

## Notes

- Always keep your backup file with original URLs (works with images from any source)
- The `url_mapping.txt` file can be reused for multiple files
- Images are automatically organized by their source directory
- Scripts handle SSL certificate issues automatically
- Scripts support images from any domain/CDN (not just specific providers) - any HTTP/HTTPS URL ending with image extensions (.png, .jpg, .jpeg, .gif, .webp, .svg)

