"""Custom filter plugins for secret generation."""

import secrets


def generate_password(length=16):
    """Generate a URL-safe random password.

    Args:
        length: Number of random bytes to use (default: 16).
                The resulting string will be longer due to base64 encoding.

    Returns:
        A URL-safe base64-encoded random string.
    """
    return secrets.token_urlsafe(length)


class FilterModule:
    """Ansible filter plugin for secret generation."""

    def filters(self):
        """Return the filter functions."""
        return {
            "generate_password": generate_password,
        }
