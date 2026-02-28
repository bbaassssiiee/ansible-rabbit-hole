"""
Ansible filter plugin for generating bcrypt hashes.
"""

import bcrypt


def bcrypt_hash(password, rounds=12, prefix=b"2a"):
    """Generate a bcrypt hash of the given password."""
    if not isinstance(rounds, int) or rounds < 4 or rounds > 31:
        rounds = 12
    if not isinstance(password, bytes):
        password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt(rounds, prefix)).decode("utf-8")


class FilterModule(object):
    """Ansible filter plugin to include custom filters."""

    def filters(self):
        """Return a dictionary of filter functions to be used in Ansible.

        Returns:
            dict: Mapping of filter names to functions.
        """
        return {"bcrypt_hash": bcrypt_hash}
