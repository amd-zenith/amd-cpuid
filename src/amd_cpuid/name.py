"""
AMD Zen processor codename lookup.
"""

# Family-level names.
_FAMILY_NAMES: dict[int, str] = {
    0x17: "Zen/Zen+/Zen2",
    0x19: "Zen3/Zen4",
    0x1a: "Zen5",
}

def lookup_family_name(family: int) -> str:
    """Return the AMD codename for the given extended family number."""
    return _FAMILY_NAMES.get(family, "Unknown")
