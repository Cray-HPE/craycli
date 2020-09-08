"""ars"""
# pylint: disable=invalid-name
from cray.generator import generate


cli = generate(__file__)

# Since this API/CLI is deprecated, hide from the main help message
cli.hidden = True
