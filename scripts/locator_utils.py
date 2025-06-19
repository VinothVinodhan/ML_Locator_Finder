# scripts/locator_utils.py

import re

def generate_locator(el) -> str:
    tag = el.name
    attrs = el.attrs

    parts = []
    # Add stable attributes, skip random IDs
    if attrs.get("name"):
        parts.append(f"name=\"{attrs['name']}\"")
    elif attrs.get("href"):
        parts.append(f"href=\"{attrs['href']}\"")
    elif attrs.get("aria-label"):
        parts.append(f"aria-label=\"{attrs['aria-label']}\"")

    # Data-text / placeholder
    for key in ["data-text", "aria-description", "placeholder", "type", "value"]:
        if attrs.get(key):
            parts.append(f"{key}=\"{attrs[key]}\"")

    # Class list
    cl = attrs.get("class")
    if cl:
        parts.append(f"class=\"{' '.join(cl)}\"")

    locator = f"{tag}"
    if parts:
        locator += "[" + "][".join(parts) + "]"
    return locator
