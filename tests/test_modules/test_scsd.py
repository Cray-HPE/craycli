# MIT License
#
# (C) Copyright [2020-2022] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

""" Test the scsd module.
"""

# pylint: disable=invalid-name,
# pylint: disable=too-many-arguments, unused-argument
import json

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import

urlPrefix = '/apis/scsd/v1'
#urlPrefix = '/v1'  # for testing



# Dictionary comparison function.  Dicts are created from JSON payloads.
# pylint: disable=redefined-outer-name
def subDiff(obj, dlist):
    """ Take a dict object and recursively walk it to produce a sorted flat KV list"""

    for k in sorted(obj):
        if isinstance(obj[k], dict):
            subDiff(obj[k],dlist)
        else:
            if isinstance(obj[k],list):
                ss = sorted(obj[k])
                dlist.append(k)
                dlist.append(ss)
            else:
                dlist.append(k)
                dlist.append(obj[k])

def findDiff(d1, d2):
    """ Compare two dicts (from JSON payloads) for equality, dict-order neutral """

    diffOK = 1
    slist1 = []
    slist2 = []
    subDiff(d1,slist1)
    subDiff(d2,slist2)
    if slist1 != slist2:
        print("Payload mismatch!")
        print(slist1)
        print("========================================================")
        print(slist2)
        diffOK = 0

    return diffOK


# pylint: disable=redefined-outer-name
def test_scsd_help_info(cli_runner, rest_mock):
    """ Test `cray scsd` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd'])
    assert result.exit_code == 0

    outputs = [
        "cli scsd [OPTIONS] COMMAND [ARGS]...",
        "bmc",
        "version"
    ]
    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_scsd_bmc(cli_runner, rest_mock):
    """ Test `cray scsd bmc` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc'])

    outputs = [
        "cli scsd bmc [OPTIONS] COMMAND [ARGS]...",
        "bios",
        "cfg",
        "createcerts",
        "creds",
        "deletecerts",
        "discreetcreds",
        "dumpcfg",
        "fetchcerts",
        "globalcreds",
        "loadcfg",
        "setcert",
        "setcerts",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_scsd_bmc_bios_tpmstate(cli_runner, rest_mock):
    """ Test `cray scsd bmc bios tpmstate` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'bios'])

    outputs = [
        "cli scsd bmc bios [OPTIONS] COMMAND [ARGS]...",
        "describe",
        "update",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_scsd_bmc_bios_tpmstate_update(cli_runner, rest_mock):
    """ Test `cray scsd bmc bios update` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/bios'
    future = 'Disabled'

    comp = 'x0c0s0b0n0'
    result = runner.invoke(cli, ['scsd', 'bmc', 'bios', 'update', 'tpmstate',
                                 '--future', future,
                                 comp])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}/{}/{}'.format(config['default']['hostname'],
                                              url_template,
                                              comp,
                                              'tpmstate')

    expdata = {
        'Future': future
    }

    ok = findDiff(expdata, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_cfg(cli_runner, rest_mock):
    """ Test `cray scsd bmc cfg` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'cfg'])

    outputs = [
        "cli scsd bmc cfg [OPTIONS] COMMAND [ARGS]...",
        "create",
        "describe",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=too-many-locals
# pylint: disable=redefined-outer-name
def test_scsd_bmc_cfg_create(cli_runner, rest_mock):
    """ Test `cray scsd bmc cfg create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/cfg'
    sshkey = 'aabbccdd'
    sshckey = 'eeffgghh'
    syspe = True
    syssv = '10.100.1.1'
    sysport = 1234
    ntppe = True
    ntpsv = '10.200.1.1'
    ntpport = 5678
    force = True

    comp = 'x0c0s0b0'
    result = runner.invoke(cli, ['scsd', 'bmc', 'cfg', 'create',
                                 '--params--ssh-console-key', sshckey,
                                 '--params--ssh-key', sshkey,
                                 '--params--syslog-server-info--protocol-enabled', syspe,
                                 '--params--syslog-server-info--port', sysport,
                                 '--params--syslog-server-info--syslog-servers', syssv,
                                 '--params--ntp-server-info--protocol-enabled', ntppe,
                                 '--params--ntp-server-info--port', ntpport,
                                 '--params--ntp-server-info--ntp-servers', ntpsv,
                                 '--force', force,
                                 comp])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

    expdata = {
        'Force': force,
        'Params': {
            'NTPServerInfo': {
                'NTPServers': ntpsv,
                'Port': ntpport,
                'ProtocolEnabled': ntppe,

            },
            'SyslogServerInfo': {
                'SyslogServers': syssv,
                'Port': sysport,
                'ProtocolEnabled': syspe,
            },
            'SSHKey': sshkey,
            'SSHConsoleKey': sshckey,
        }
    }

    ok = findDiff(expdata, data['body'])
    assert(ok == 1)


# pylint: disable=redefined-outer-name
def test_scsd_bmc_cfg_describe(cli_runner, rest_mock):
    """ Test `cray scsd bmc cfg describe` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/cfg'
    comp = 'x0c0s0b0'

    result = runner.invoke(cli, ['scsd', 'bmc', 'cfg', 'describe',
                                 '--param', 'NTPServerInfo,SyslogServerInfo,SSHKey,SSHConsoleKey',
                                 comp])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}?{}'.format(
        config['default']['hostname'],
        url_template,
        comp,
        'param=NTPServerInfo%2CSyslogServerInfo%2CSSHKey%2CSSHConsoleKey'
    )

# pylint: disable=redefined-outer-name
def test_scsd_bmc_loadcfg(cli_runner, rest_mock):
    """ Test `cray scsd bmc loadcfg` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'loadcfg'])

    outputs = [
        "cli scsd bmc loadcfg [OPTIONS] COMMAND [ARGS]...",
        "create",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_scsd_bmc_loadcfg_create(cli_runner, rest_mock):
    """ Test `cray scsd bmc loadcfg create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/loadcfg'

    payload_json = '''{
        "Force": true,
        "Targets": [
            "x0c0s0b0",
            "x0c0s1b0"
        ],
        "Params": {
            "NTPServerInfo": {
                "NTPServers": ["sms-nnn"],
                "Port": 1234,
                "ProtocolEnabled": true
            },
            "SyslogServerInfo": {
                "SyslogServers": ["sms-sss"],
                "Port": 5678,
                "ProtocolEnabled": true
            },
            "SSHKey": "aa11bb22",
            "SSHConsoleKey": "cc33dd44"
        }
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'loadcfg', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_dumpcfg_create(cli_runner, rest_mock):
    """ Test `cray scsd bmc dumpcfg create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/dumpcfg'

    payload_json = '''{
        "Targets": [
            "x0c0s0b0",
            "x0c0s1b0"
        ],
        "Params": [
            "NTPServerInfo",
            "SyslogServerInfo",
            "SSHKey",
            "SSHConsoleKey"
        ]
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'dumpcfg', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)


# pylint: disable=redefined-outer-name
def test_scsd_bmc_creds(cli_runner, rest_mock):
    """ Test `cray scsd bmc creds` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'creds'])

    outputs = [
        "cli scsd bmc creds [OPTIONS] COMMAND [ARGS]...",
        "create",
        "list",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_scsd_bmc_creds_create(cli_runner, rest_mock):
    """ Test `cray scsd bmc creds create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/creds'

    credsuname = 'cred_user'
    credspw = 'cred_pw'
    force = True
    comp = 'x0c0s0b0'

    result = runner.invoke(cli, ['scsd', 'bmc', 'creds', 'create',
                                 '--creds--username', credsuname,
                                 '--creds--password', credspw,
                                 '--force', force,
                                 comp, ])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)
    payload = {
        'Force': force,
        'Creds': {
            "Username": credsuname,
            "Password": credspw,
        }
    }
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_discreetcreds_create(cli_runner, rest_mock):
    """ Test `cray scsd bmc discreetcreds create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/discreetcreds'

    payload_json = '''{
        "Force": true,
        "Targets": [
        {
            "Xname": "x0c0s0b0",
            "Creds": {
                "Username":"b0_user",
                "Password":"b0_pw"
            }
        }
        ]
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'discreetcreds', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_globalcreds_create(cli_runner, rest_mock):
    """ Test `cray scsd bmc globalcreds create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/globalcreds'

    payload_json = '''{
        "Force": true,
        "Username":"glb_user",
        "Password":"glb_pw",
        "Targets": [
            "x0c0s0b0",
            "x0c0s1b0"
        ]
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'globalcreds', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_creds_list(cli_runner, rest_mock):
    """ Test `cray scsd bmc list` """
    runner, cli, opts = cli_runner
    url_template = urlPrefix+'/bmc/creds'
    config = opts['default']
    hostname = config['hostname']
    targName = 'x1000c0s1b0'
    targType = 'NodeBMC'

    result = runner.invoke(cli, ['scsd', 'bmc', 'creds', 'list',
                                 '--targets', targName,
                                 '--type', targType])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'].lower() == 'get'
    uri = data['url'].split(hostname)[-1]
    outputs = [
        url_template,
        "targets="+targName,
        "type="+targType,
    ]

    for out in outputs:
        assert out in uri


# pylint: disable=redefined-outer-name
def test_scsd_bmc_createcerts(cli_runner, rest_mock):
    """" Test `cray scsd bmc createcerts` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'createcerts'])

    outputs = [
        "cli scsd bmc createcerts [OPTIONS] COMMAND [ARGS]...",
        "create",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_scsd_bmc_createcerts_create(cli_runner, rest_mock):
    """" Test `cray scsd bmc createcerts create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/createcerts'

    payload_json = '''{
        "Domain": "Cabinet",
        "DomainIDs": [
            "x0c0s0b0"
        ]
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'createcerts', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_deletecerts(cli_runner, rest_mock):
    """" Test `cray scsd bmc deletecerts` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'deletecerts'])

    outputs = [
        "cli scsd bmc deletecerts [OPTIONS] COMMAND [ARGS]...",
        "create",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


# pylint: disable=redefined-outer-name
def test_scsd_bmc_deletecerts_delete(cli_runner, rest_mock):
    """" Test `cray scsd bmc deletecerts create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/deletecerts'

    payload_json = '''{
        "Domain": "Cabinet",
        "DomainIDs": [
            "x0c0s0b0"
        ]
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'deletecerts', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_fetchcerts(cli_runner, rest_mock):
    """" Test `cray scsd bmc fetchcerts` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'fetchcerts'])

    outputs = [
        "cli scsd bmc fetchcerts [OPTIONS] COMMAND [ARGS]...",
        "create",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0


# pylint: disable=redefined-outer-name
def test_scsd_bmc_fetchcerts_create(cli_runner, rest_mock):
    """" Test `cray scsd bmc fetchcerts create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/fetchcerts'

    payload_json = '''{
        "Domain": "Cabinet",
        "DomainIDs": [
            "x0c0s0b0"
        ]
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'fetchcerts', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_setcerts(cli_runner, rest_mock):
    """" Test `cray scsd bmc setcerts` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'setcerts'])

    outputs = [
        "cli scsd bmc setcerts [OPTIONS] COMMAND [ARGS]...",
        "create",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

# pylint: disable=redefined-outer-name
def test_scsd_bmc_setcerts_create(cli_runner, rest_mock):
# This one is capable of multiple targets from file.  Test will only use one target.
    """" Test `cray scsd bmc setcerts create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/setcerts'

    payload_json = '''{
        "Force": false,
        "CertDomain": "Cabinet",
        "Targets": [
            "x0c0s0b0"
        ]
    }'''
    payload = json.loads(payload_json)

    with open('test.json', 'w', encoding='utf-8') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'setcerts', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    ok = findDiff(payload, data['body'])
    assert(ok == 1)

# pylint: disable=redefined-outer-name
def test_scsd_bmc_setcert_create(cli_runner, rest_mock):
# This one is the single {xname} version
    """ Test `cray scsd bmc setcert create` """

    runner, cli, config = cli_runner
    url_template = urlPrefix+'/bmc/setcert'

    domain = 'Cabinet'
    force = True
    comp = 'x0c0s0b0'
    qstr = '''?Force=True&Domain=Cabinet'''

    result = runner.invoke(cli, ['scsd', 'bmc', 'setcert', 'create',
                                 '--domain', domain,
                                 '--force', force,
                                 comp, ])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}/{}{}'.format(config['default']['hostname'],
                                             url_template, comp, qstr)
