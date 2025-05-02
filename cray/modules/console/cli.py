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
""" Console - websocket interaction with console services """
# pylint: disable=invalid-name,redefined-outer-name,missing-docstring,unused-argument,broad-except,too-many-locals,too-many-branches,too-many-statements
import asyncio
import json
import click
import websockets
import aioconsole

from cray.constants import TENANT_HEADER_NAME_KEY
from cray.core import argument
from cray.core import group
from cray.core import pass_context
from cray.core import option

# Header name keys for console apis
CONSOLE_HEADER_TAIL_KEY = "Cray-Console-Lines"
CONSOLE_HEADER_FOLLOW_KEY = "Cray-Console-Follow"

@group()
def cli():
    """ Interact with node consoles """
    pass

###########################################################################
# helper function to run the websocket terminal interaction
###########################################################################
async def websocket_terminal_interaction(ctx, endpoint: str, headers: dict[str,str]) -> str:
    # set up the return value
    errMsg = ""

    #raise AssertionError("Harf")

    # pull information from context
    config = ctx.obj['config']
    auth = ctx.obj["auth"]
    globals_ctx = ctx.obj['globals']
    tenant = config.get('core.tenant', "")
    hostname = config.get('core.hostname', "")

    # add auth header
    token = ""
    if auth and auth.session and auth.session.access_token:        
        token = auth.session.access_token
    else:
        raise AssertionError(str(globals_ctx))
        if globals_ctx and globals_ctx.token.access_token:        
            token = globals_ctx.token.access_token
    if token != "":
        headers["Authorization"] = f"Bearer {token}"

    # add tenant header
    if tenant:
        headers[TENANT_HEADER_NAME_KEY] = tenant

    # pull the hostname from the context
    if hostname !="":
        # if the hostname has a scheme, remove it
        loc = hostname.find('://')
        if loc != -1:
            hostname = hostname[loc + 3:]

    # if the hostname is not set, use the default
    if not hostname:
        # if the hostname is still not set, use the default
        hostname = 'api-gw-service-nmn.local'

    # build the uri from the hostname and endpoint - note secure websocket
    uri = f"wss://{hostname}/{endpoint}"

    if hostname:
        raise AssertionError("Harf")

    try:
        # connect to the websocket
        async with websockets.connect(uri, additional_headers=headers) as websocket:
            print(f"Connected to {uri}")

            async def send_messages():
                while True:
                    try:
                        message = await aioconsole.ainput("")
                        await websocket.send(message)
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        print(f"Error sending message: {e}")
                        break

            async def receive_messages():
                while True:
                    try:
                        message = await websocket.recv()
                        print(f"{message}", end='', flush=True)
                    except websockets.ConnectionClosed:
                        print("Connection closed by the server.")
                        break
                    except Exception as e:
                        print(f"Error receiving message: {e}")
                        break

            send_task = asyncio.create_task(send_messages())
            receive_task = asyncio.create_task(receive_messages())

            _, pending = await asyncio.wait(
                [send_task, receive_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()
    except websockets.InvalidStatus as e:
        # Expect this to be an unauthorized tenant, try to pull details
        # from the response body
        errMsg = "Websocket connection failed"
        body = e.response.body
        if body:
            try:
                data = json.loads(body.decode('utf-8'))
                errMsg = f"{data.get('message', errMsg)}"
            except json.JSONDecodeError:
                # if the body is not json, just decode it
                errMsg = f"{body.decode('utf-8')}"
    except websockets.ConnectionClosed as e:
        # handle the connection getting closed
        errMsg = f"Connection closed: {e}"
    except Exception as e:
        # gracefully handle any other exceptions
        errMsg = f"Error: {e}"

    return errMsg

###########################################################################
# cray console interact
###########################################################################
@cli.command(name='interact')
@argument('xname', metavar='XNAME',required=True, type=click.STRING, nargs=1)
@pass_context
def interact(ctx, xname):
    # Interact with the console.
    headers = {}
    endpoint = f"apis/console-operator/console-operator/interact/{xname}"
    errMsg = asyncio.run(websocket_terminal_interaction(ctx, endpoint, headers))

    # if there was an error, print the help, then the error message
    if errMsg:
        click.echo(ctx.get_help())
        print(f"\n\nERROR: {errMsg}")

###########################################################################
# cray console log
###########################################################################
@cli.command(name='tail')
@argument('xname', metavar='XNAME',required=True, type=click.STRING, nargs=1)
@option(
    '--lines', '-n', multiple=False,
    type=click.INT, required=False,
    default=10,
    show_default=True,
    help='Optionally the number of existing lines to output.'
)
@option(
    '--follow', '-f', multiple=False,
    type=click.BOOL, required=False,
    is_flag=True,
    default=False,
    show_default=True,
    help='Follow the log information after displaying the current log.'
)
@pass_context
def tail(ctx, xname, lines, follow):
    # Tail the console output.

    # pull out the options and load into the headers
    headers = {}
    if lines:
        headers[CONSOLE_HEADER_TAIL_KEY] = str(lines)
    if follow:
        headers[CONSOLE_HEADER_FOLLOW_KEY] = str(follow)

    # open the websocket
    endpoint = f"apis/console-operator/console-operator/tail/{xname}"
    errMsg = asyncio.run(websocket_terminal_interaction(ctx, endpoint, headers))

    # if there was an error, print the help, then the error message
    if errMsg:
        click.echo(ctx.get_help())
        print(f"\n\nERROR: {errMsg}")
