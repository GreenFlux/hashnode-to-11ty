# Hashnode to 11ty Converter (h2e)

A Python CLI tool for converting Hashnode blog exports to 11ty-compatible format. This is a  one-time migration tool to move your Hashnode data to 11ty. 

## 🎯 Features

- **Parse Hashnode exports** - Load and validate JSON export files
- **API enrichment** - Fetch missing tag names, series info via Hashnode GraphQL API
- **Content transformation** - Convert to 11ty markdown with proper frontmatter
- **Image processing** - Download image from Hashnode server and organize locally
- **Offline capability** - Works without API using fallback mode
- **Progress tracking** - Visual progress bars and detailed logging
- **Dry run mode** - Preview changes without writing files

## 🚀 Quick Start

### 1. Set Up Environment

```bash
# Create virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Hashnode API (Optional but Recommended)

**🎯 For best results, set up API access first - this converts tag IDs to readable names!**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Get your API key at: https://hashnode.com/settings/developer
```

Your `.env` file should look like:
```env
HASHNODE_API_KEY=your_actual_api_key_here
```

**⚠️ Without API key:** Tags will show as cryptic IDs (e.g., "Tag-6547328" instead of "JavaScript"). You can still use the tool with `--skip-enrichment` flag.

### 3. Get Your Hashnode Export

1. Go to your **Hashnode Dashboard**
2. Navigate to **Blog Settings** → **Export**
3. Click **"Download all your articles"** to get your blog data as JSON
4. Save the file in this directory (e.g., `my-export.json`)

### 4. Basic Usage


```bash
# Quick test with 2 posts (recommended first run)
python h2e.py my-export.json --output ./test --limit 2 --dry-run

# Full conversion with API enrichment
python h2e.py my-export.json --output ./blog

# Offline mode (no API key needed)
python h2e.py my-export.json --output ./blog --skip-enrichment --skip-images
```

## 📋 Command Reference

### Basic Syntax
```bash
python h2e.py [EXPORT_FILE] [OPTIONS]
```

### Options
- `--output, -o PATH` - Output directory (default: `./output`)
- `--limit, -l N` - Limit posts for testing (e.g., `--limit 5`)
- `--skip-enrichment` - Skip API calls (tags show as IDs)
- `--skip-images` - Skip image downloads (use remote URLs)
- `--api-key TEXT` - Hashnode API key (overrides env var)
- `--dry-run` - Preview without writing files
- `--verbose, -v` - Enable detailed output

## 🧪 Testing Examples

```bash
# Test with sample data (uses included example)
python h2e.py hashnode-export-example.json --output ./test --limit 2 --dry-run

# Test your export (recommended workflow)
python h2e.py my-export.json --output ./test --limit 2 --skip-enrichment --skip-images --dry-run

# Full test with API but no images
python h2e.py my-export.json --output ./test --limit 5 --skip-images --dry-run

# Production conversion
python h2e.py my-export.json --output ./my-blog
```

## 📁 Output Structure

The tool generates 11ty-compatible files:

```
output/
├── content/
│   └── posts/
│       ├── posts.json           # Collection configuration
│       ├── my-first-post.md     # Individual post files
│       └── another-post.md
├── _data/
│   ├── metadata.json            # Site metadata
│   ├── allTags.json            # Tags data
│   └── allSeries.json          # Series data
└── images/                      # Only if images downloaded
    └── posts/
        ├── my-first-post/       # Post-specific images
        │   ├── cover.jpg
        │   └── content_1.png
        └── another-post/
            └── cover.jpg
```

## 🏷️ Generated Frontmatter

Each post gets proper 11ty frontmatter:

```yaml
---
title: "My Blog Post"
date: 2024-01-15
permalink: "/my-blog-post/"
layout: "post"
excerpt: "A brief description of the post"
coverImage: "/images/posts/my-blog-post/cover.jpg"
readTime: 8
tags: ["JavaScript", "Tutorial"]
series: "Web Development Basics"
---

Post content in clean markdown...
```

## 🔄 Reset and Cleanup

### Quick Reset
```bash
# Remove test outputs
rm -rf test* output* blog*

# Clean Python cache
find . -name "__pycache__" -delete
find . -name "*.pyc" -delete
```

### Reset Script
```bash
# Use the included reset script
./reset.sh
```

## 🔧 API Enrichment

### With API Key
When you provide a Hashnode API key:
- ✅ Converts tag IDs to readable names (e.g., "JavaScript" instead of "6547328...")
- ✅ Fetches series descriptions and metadata
- ✅ Gets accurate publication information
- ✅ Ensures data consistency

### Without API Key (Fallback Mode)
Using `--skip-enrichment`:
- ⚠️ Tags show as shortened IDs (e.g., "Tag-6547328")
- ⚠️ Series info is limited to basic data
- ✅ All other features work normally
- ✅ Faster processing, works offline

## 🖼️ Image Processing

### With Image Downloads (Default)
- Downloads cover images and content images
- Organizes them into `images/posts/{slug}/` structure
- Updates markdown to use local paths
- Shows download progress and statistics
- Handles failed downloads gracefully

### Skip Images (`--skip-images`)
- Uses original remote URLs from Hashnode
- No local image storage
- Faster processing
- Depends on Hashnode servers remaining online

## 🐛 Troubleshooting

### Common Issues


**❌ "HASHNODE_API_KEY environment variable is required"**
```bash
# Problem: No API key set
# Solution: Either set key or skip enrichment
echo "HASHNODE_API_KEY=your_key" > .env
# OR
python h2e.py export.json --skip-enrichment
```

**❌ "GraphQL errors" or "400 Client Error"**
```bash
# Problem: API key invalid or posts not accessible
# Solution: Use fallback mode
python h2e.py export.json --skip-enrichment
```

## 🤝 Contributing

Found a bug or have a feature request? Feel free to submit an issue. 

## 📄 License

MIT License - feel free to use and modify for your blog migration needs.