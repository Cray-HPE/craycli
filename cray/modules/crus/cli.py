"""CRUS - Compute Rolling Upgrade Service
"""
from cray.generator import generate
cli = generate(__file__, condense=False)  # pylint: disable=invalid-name
