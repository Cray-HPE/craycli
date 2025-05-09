#
#  MIT License
#
#  (C) Copyright 2025 Hewlett Packard Enterprise Development LP
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#
""" Tests for Console Services CLI subcommand (`cray console`)
and options. """
# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=line-too-long

def test_cray_console_base(cli_runner, rest_mock):
    """ Test cray console base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['console'])
    assert result.exit_code == 0

    outputs = [
        "interact",
        "tail"
    ]
    for txt in outputs:
        assert txt in result.output

def test_cray_console_interact(cli_runner, rest_mock):
    """ Test cray console interact ... """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['console', 'interact', 'foo'])
    assert result.exit_code == 0
    # NOTE: this is a websocket connection, so we can't test the output

def test_cray_console_tail(cli_runner, rest_mock):
    """ Test cray console tail ... """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['console', 'tail', 'foo'])
    assert result.exit_code == 0
    # NOTE: this is a websocket connection, so we can't test the output
