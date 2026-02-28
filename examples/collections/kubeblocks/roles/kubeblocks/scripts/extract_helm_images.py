#!/usr/bin/env python3
"""
Extract Docker image URLs from Helm charts (tgz format).
Usage: python extract_helm_images.py <directory>
"""

import sys
import os
import tarfile
import yaml
import re
from pathlib import Path
from typing import Set, List


def extract_images_from_values(values: dict, images: Set[str], path: str = "") -> None:
    """Recursively extract image references from values.yaml"""
    if isinstance(values, dict):
        # Common patterns for image definitions
        if 'image' in values:
            img = values['image']
            if isinstance(img, str):
                images.add(img)
            elif isinstance(img, dict):
                # Handle image.repository and image.tag pattern
                repository = img.get('repository', '')
                tag = img.get('tag', '')
                registry = img.get('registry', '')

                if repository:
                    # Build full image reference
                    # Skip docker.io registry as it's the default
                    if registry and registry != 'docker.io':
                        image = f"{registry}/{repository}"
                    else:
                        image = repository

                    # Handle tag that might be a dict (multiple versions)
                    if isinstance(tag, dict):
                        # Flatten nested tag dictionaries
                        tags = []
                        def flatten_dict(d):
                            for v in d.values():
                                if isinstance(v, dict):
                                    flatten_dict(v)
                                else:
                                    tags.append(str(v))
                        flatten_dict(tag)

                        for t in tags:
                            images.add(f"{image}:{t}")
                    elif tag:
                        image = f"{image}:{tag}"
                        images.add(image)
                    else:
                        # Add latest if no tag specified
                        images.add(f"{image}:latest")

        # Also check for standalone repository and tag at same level
        if 'repository' in values and not isinstance(values.get('image'), dict):
            repo = values.get('repository', '')
            tag = values.get('tag', 'latest')
            registry = values.get('registry', '')

            if repo:
                # Skip docker.io registry as it's the default
                if registry and registry != 'docker.io':
                    base_image = f"{registry}/{repo}"
                else:
                    base_image = repo

                # Handle tag that might be a dict (multiple versions)
                if isinstance(tag, dict):
                    tags = []
                    def flatten_dict(d):
                        for v in d.values():
                            if isinstance(v, dict):
                                flatten_dict(v)
                            else:
                                tags.append(str(v))
                    flatten_dict(tag)

                    for t in tags:
                        images.add(f"{base_image}:{t}")
                else:
                    images.add(f"{base_image}:{tag}")

        # Recurse into nested dictionaries
        for key, value in values.items():
            extract_images_from_values(value, images, f"{path}.{key}" if path else key)

    elif isinstance(values, list):
        for item in values:
            extract_images_from_values(item, images, path)


def extract_images_from_templates(template_content: str, images: Set[str]) -> None:
    """Extract image references from template files using regex"""
    # Pattern for image: "registry/repo:tag" or image: registry/repo:tag
    patterns = [
        r'image:\s*["\']?([a-zA-Z0-9._/-]+:[a-zA-Z0-9._-]+)["\']?',
        r'image:\s*["\']?([a-zA-Z0-9._/-]+/[a-zA-Z0-9._/-]+)["\']?',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, template_content)
        images.update(matches)


def process_helm_chart(chart_path: Path) -> Set[str]:
    """Extract all image URLs from a Helm chart tgz file"""
    images = set()

    try:
        with tarfile.open(chart_path, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.name.endswith('values.yaml') or member.name.endswith('values.yml'):
                    f = tar.extractfile(member)
                    if f:
                        content = f.read()
                        try:
                            values = yaml.safe_load(content)
                            extract_images_from_values(values, images)
                        except yaml.YAMLError as e:
                            print(f"Warning: Could not parse {member.name} in {chart_path}: {e}", file=sys.stderr)

                # Also check template files
                elif '/templates/' in member.name and member.isfile():
                    f = tar.extractfile(member)
                    if f:
                        content = f.read().decode('utf-8', errors='ignore')
                        extract_images_from_templates(content, images)

    except Exception as e:
        print(f"Error processing {chart_path}: {e}", file=sys.stderr)

    return images


def find_helm_charts(directory: Path) -> List[Path]:
    """Recursively find all .tgz files in directory"""
    return list(directory.rglob('*.tgz'))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>", file=sys.stderr)
        sys.exit(1)

    directory = Path(sys.argv[1])

    if not directory.exists():
        print(f"Error: Directory {directory} does not exist", file=sys.stderr)
        sys.exit(1)

    if not directory.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    chart_files = find_helm_charts(directory)

    if not chart_files:
        print(f"No Helm charts (.tgz) found in {directory}", file=sys.stderr)
        sys.exit(0)

    print(f"# Found {len(chart_files)} Helm chart(s)", file=sys.stderr)

    all_images = set()

    for chart_path in chart_files:
        print(f"# Processing {chart_path}", file=sys.stderr)
        images = process_helm_chart(chart_path)
        all_images.update(images)

    # Print unique images, one per line
    for image in sorted(all_images):
        # Remove docker.io prefix if present
        if image.startswith('docker.io/'):
            image = image[10:]  # Remove 'docker.io/' prefix

        if image and ':' in image:  # Only output images with tags
            print(image)
        elif image and ':' not in image:  # Add latest tag if missing
            print(f"{image}:latest")

    print(f"# Total unique images: {len(all_images)}", file=sys.stderr)


if __name__ == '__main__':
    main()
