# Helm Charts Downloader

Two Python scripts to scrape and download Helm charts from ApeCloud repository with mirror directory structure.

## Scripts

### 1. scrape_helm_charts.py
Scrapes v1.0.1 charts from the Helm repository index and saves metadata to YAML.

**Usage:**
```bash
python3 scrape_helm_charts.py
```

**Output:** `charts_v1.0.1.yaml` - Contains filtered chart metadata with download URLs

### 2. download_charts.py
Downloads all .tgz chart files from the scraped YAML file into a mirror directory structure.

**Basic Usage:**
```bash
python3 download_charts.py
```

**Advanced Usage:**
```bash
# Custom input file
python3 download_charts.py -i charts_v1.0.1.yaml

# Custom output directory
python3 download_charts.py -o /path/to/mirror

# Custom base URL (for different sources)
python3 download_charts.py -b "https://example.com/charts/"

# All options combined
python3 download_charts.py -i charts_v1.0.1.yaml -o /path/to/mirror -b "https://github.com/apecloud/helm-charts/releases/download/"
```

**Options:**
- `-i, --input`: Input YAML file (default: charts_v1.0.1.yaml)
- `-o, --output`: Output directory (default: downloaded_charts)
- `-b, --base-url`: Base URL to strip from chart URLs for creating relative paths (default: https://github.com/apecloud/helm-charts/releases/download/)

## Complete Workflow

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Scrape chart metadata
python3 scrape_helm_charts.py

# Step 3: Download all charts with mirror structure
python3 download_charts.py
```

## Features

### scrape_helm_charts.py
- Fetches Helm repository index
- Handles Chinese characters properly
- Filters charts by version (1.0.1)
- Exports metadata to YAML

### download_charts.py
- Downloads all chart .tgz files
- Creates mirror directory structure (each chart in its own subdirectory)
- Shows progress for each download
- Skips already downloaded files
- Provides download summary
- Perfect for creating Helm chart mirrors

## Output Structure

The download script creates a mirror-ready directory structure:

```
downloaded_charts/
├── apecloud-mysql-1.0.1/
│   └── apecloud-mysql-1.0.1.tgz
├── apecloud-mysql-cluster-1.0.1/
│   └── apecloud-mysql-cluster-1.0.1.tgz
├── kafka-1.0.1/
│   └── kafka-1.0.1.tgz
├── redis-1.0.1/
│   └── redis-1.0.1.tgz
└── ...
```

This structure matches the URL pattern:
```
https://github.com/apecloud/helm-charts/releases/download/apecloud-mysql-1.0.1/apecloud-mysql-1.0.1.tgz
                                                            └────────────────┬────────────────┘
                                                                  Becomes subdirectory
```

## Creating a Helm Chart Mirror

After downloading, you can serve the charts as a mirror:

### Option 1: Simple HTTP Server
```bash
cd downloaded_charts
python3 -m http.server 8080
```

### Option 2: Nginx
```nginx
server {
    listen 80;
    server_name your-mirror.example.com;
    root /path/to/downloaded_charts;
    autoindex on;
}
```

### Option 3: Object Storage (S3, MinIO, etc.)
```bash
# Upload to S3
aws s3 sync downloaded_charts/ s3://your-bucket/helm-charts/ --acl public-read

# Upload to MinIO
mc mirror downloaded_charts/ myminio/helm-charts/
```

Then update your Helm repo URL:
```bash
# Original
helm repo add apecloud https://github.com/apecloud/helm-charts/releases/download/

# Your mirror
helm repo add apecloud https://your-mirror.example.com/
```

## Requirements

- Python 3.6+
- requests
- PyYAML

## Notes

- The download script will skip files that already exist
- All downloads include progress indicators
- Failed downloads are reported in the summary
- The mirror structure preserves the original URL hierarchy for easy mirroring
