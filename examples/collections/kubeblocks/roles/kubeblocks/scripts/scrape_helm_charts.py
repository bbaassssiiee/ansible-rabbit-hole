#!/usr/bin/env python3
"""
Scrape v1.0.1 charts from ApeCloud Helm repository index
"""

import requests
import yaml
from typing import Dict, List
import re


def fetch_helm_index(url: str) -> Dict:
    """Fetch and parse the Helm repository index.yaml file"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Get content as bytes and decode properly
        content = response.content

        # Try UTF-8 first
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to GB18030 for Chinese characters
            try:
                text = content.decode('gb18030')
            except UnicodeDecodeError:
                # Last resort: latin-1 which accepts all bytes
                text = content.decode('latin-1')

        # Parse YAML with full loader to handle all content
        return yaml.load(text, Loader=yaml.FullLoader)

    except requests.RequestException as e:
        print(f"Error fetching index: {e}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}


def filter_charts_by_version(index_data: Dict, target_version: str) -> Dict[str, List[Dict]]:
    """Filter charts by specific version"""
    filtered_charts = {}

    entries = index_data.get('entries', {})

    for chart_name, versions in entries.items():
        matching_versions = [
            chart for chart in versions
            if chart.get('version') == target_version
        ]

        if matching_versions:
            filtered_charts[chart_name] = matching_versions

    return filtered_charts


def contains_chinese(text: str) -> bool:
    """Check if text contains Chinese characters"""
    if not text:
        return False
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def display_charts(charts: Dict[str, List[Dict]]):
    """Display the filtered charts in a readable format"""
    if not charts:
        print("No charts found with version 1.0.1")
        return

    print(f"\nFound {len(charts)} chart(s) with version 1.0.1:\n")
    print("=" * 80)

    for chart_name, versions in charts.items():
        for chart in versions:
            print(f"\nChart Name: {chart_name}")
            print(f"Version: {chart.get('version')}")
            print(f"App Version: {chart.get('appVersion', 'N/A')}")

            # Handle description with Chinese characters
            description = chart.get('description', 'N/A')
            if contains_chinese(str(description)):
                print(f"Description (Chinese): {description}")
            else:
                print(f"Description: {description}")

            print(f"Created: {chart.get('created', 'N/A')}")

            # Display URLs
            urls = chart.get('urls', [])
            if urls:
                print(f"Download URL: {urls[0]}")

            # Display maintainers if available
            maintainers = chart.get('maintainers', [])
            if maintainers:
                print("Maintainers:")
                for maintainer in maintainers:
                    name = maintainer.get('name', 'Unknown')
                    email = maintainer.get('email', '')
                    print(f"  - {name}" + (f" ({email})" if email else ""))

            print("-" * 80)


def main():
    repo_url = "https://apecloud.github.io/helm-charts/index.yaml"
    target_version = "1.0.1"

    print(f"Fetching Helm repository index from: {repo_url}")
    index_data = fetch_helm_index(repo_url)

    if not index_data:
        print("Failed to fetch or parse the index file")
        return

    print(f"Filtering charts for version: {target_version}")
    filtered_charts = filter_charts_by_version(index_data, target_version)

    display_charts(filtered_charts)

    # Optionally save to a file
    if filtered_charts:
        output_file = "index.yaml"
        with open(output_file, 'w') as f:
            yaml.dump(filtered_charts, f, default_flow_style=False)
        print(f"\nFiltered charts saved to: {output_file}")


if __name__ == "__main__":
    main()
