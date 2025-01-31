# cray/modules/rr/__init__.py
from .cli import cli  # <-- Explicitly import the CLI group

def setup(main_cli):
    main_cli.add_command(cli)  # <-- Add the renamed group to the main CLI