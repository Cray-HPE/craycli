""" Generates the pets swagger file as commands """
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument, import-error
import pytest

from cray import cli, generator


@pytest.fixture()
def pets():
    """Fixture to add pets swagger generated commands"""

    @cli.cli.group(name='pets')
    def stub():
        """ Unit Test CLI """
        pass

    generator.generate(__file__, '../files/swagger3.json', cli=stub)
