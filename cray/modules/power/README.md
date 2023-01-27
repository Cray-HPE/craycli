# Cray Power Control Service CLI

The CLI for this service does not leverage the automatic generation feature of many other
services. The CLI is hand-coded in the [`cli.py`](cli.py) file. That is what should be edited
when making changes to the CLI. When updating [`swagger3.json`](swagger3.json) from the source
API spec, clear out the entries from the `paths` field in the JSON file, to ensure that they
are not used by the CLI.
