""" Test the scsd module."""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
import json
import os

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock

urlPrefix = '/apis/scsd/v1'
#urlPrefix = '/v1'  # for testing

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

def test_scsd_bmc(cli_runner, rest_mock):
    """ Test `cray scsd bmc` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc'])

    outputs = [
        "cli scsd bmc [OPTIONS] COMMAND [ARGS]...",
        "cfg",
        "creds",
        "discreetcreds",
        "dumpcfg",
        "globalcreds",
        "loadcfg",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

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
    assert data['body'] == {
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
    assert data['url'] == '{}{}/{}?{}'.format(config['default']['hostname'], 
                                              url_template, 
                                              comp, 
                                              'param=NTPServerInfo%2CSyslogServerInfo%2CSSHKey%2CSSHConsoleKey')

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

    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'loadcfg', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == payload

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

    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'dumpcfg', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == payload


def test_scsd_bmc_creds(cli_runner, rest_mock):
    """ Test `cray scsd bmc creds` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['scsd', 'bmc', 'creds'])

    outputs = [
        "cli scsd bmc creds [OPTIONS] COMMAND [ARGS]...",
        "create",
    ]

    for out in outputs:
        assert out in result.output
    assert result.exit_code == 0

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
    assert data['body'] == {
        'Force': force,
        'Creds': {
            "Username": credsuname,
            "Password": credspw,
        }
    }

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

    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'discreetcreds', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == payload

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

    with open('test.json', 'w') as fp:
        json.dump(payload, fp)

    result = runner.invoke(cli, ['scsd', 'bmc', 'globalcreds', 'create',
                                 'test.json'])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == payload

