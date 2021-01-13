"""fabric controller"""
# pylint: disable=invalid-name
from cray.generator import generate

cli = generate(__file__)

# Since this is internal, hide from the main help message
cli.hidden = True
