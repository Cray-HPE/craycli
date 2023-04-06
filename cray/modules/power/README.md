# Cray Power Control Service CLI

The CLI for this service does not leverage the automatic generation feature of many other services. The CLI is
hand-coded in the [`cli.py`](cli.py) file. That is what must be edited when making changes to the CLI for PCS. While the
Swagger spec files in this folder should still be kept up to date, the information from the `paths` field in
the [`swagger3.json`](swagger3.json)
file is not used to generate the CLI.
