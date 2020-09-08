"""hsm"""
# pylint: disable=invalid-name
from cray.generator import generate


cli = generate(__file__, swagger_opts={'vocabulary':{'put':'replace', 'deleteall':'clear'}})
