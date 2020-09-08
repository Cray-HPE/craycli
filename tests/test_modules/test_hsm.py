""" Test the hsm module."""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument
import json
import os

from ..utils.runner import cli_runner
from ..utils.rest import rest_mock

def test_cray_hsm(cli_runner, rest_mock):
    """ Test `cray hsm` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "defaults",
        "groups",
        "inventory",
        "locks",
        "memberships",
        "partitions",
        "service",
        "state",
        "sysinfo"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_help(cli_runner, rest_mock):
    """ Test `cray hsm --help` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "defaults",
        "groups",
        "inventory",
        "locks",
        "memberships",
        "partitions",
        "service",
        "state",
        "sysinfo"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_service_ready_list(cli_runner, rest_mock):
    """ Test `cray hsm service ready list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/ready'
    result = runner.invoke(cli, ['hsm', 'service', 'ready', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_liveness_list(cli_runner, rest_mock):
    """ Test `cray hsm service liveness list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/liveness'
    result = runner.invoke(cli, ['hsm', 'service', 'liveness', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values(cli_runner, rest_mock):
    """ Test `cray hsm service values` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'service', 'values'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm service values [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "arch",
        "class",
        "flag",
        "nettype",
        "role",
        "state",
        "subrole",
        "type",
        "Commands:",
        "list"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_service_values_help(cli_runner, rest_mock):
    """ Test `cray hsm service values --help` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'service', 'values', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm service values [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "arch",
        "class",
        "flag",
        "nettype",
        "role",
        "state",
        "subrole",
        "type",
        "Commands:",
        "list"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_service_values_arch_list(cli_runner, rest_mock):
    """ Test `cray hsm service values arch list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/arch'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'arch', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values_class_list(cli_runner, rest_mock):
    """ Test `cray hsm service values class list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/class'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'class', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values_flag_list(cli_runner, rest_mock):
    """ Test `cray hsm service values flag list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/flag'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'flag', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values_nettype_list(cli_runner, rest_mock):
    """ Test `cray hsm service values nettype list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/nettype'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'nettype', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values_role_list(cli_runner, rest_mock):
    """ Test `cray hsm service values role list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/role'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'role', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values_state_list(cli_runner, rest_mock):
    """ Test `cray hsm service values state list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/state'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'state', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values_subrole_list(cli_runner, rest_mock):
    """ Test `cray hsm service values subrole list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/subrole'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'subrole', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_service_values_type_list(cli_runner, rest_mock):
    """ Test `cray hsm service values type list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/service/values/type'
    result = runner.invoke(cli, ['hsm', 'service', 'values', 'type', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_state_components(cli_runner, rest_mock):
    """ Test `cray hsm state components` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'state', 'components'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm state components [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "bulkEnabled",
        "bulkFlagOnly",
        "bulkNID",
        "bulkRole",
        "bulkSoftwareStatus",
        "bulkStateData",
        "byNID",
        "enabled",
        "flagOnly",
        "nID",
        "query",
        "role",
        "softwareStatus",
        "stateData",
        "Commands:",
        "clear",
        "create",
        "delete",
        "describe",
        "list",
        "replace"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_state_components_help(cli_runner, rest_mock):
    """ Test `cray hsm state components --help` with valid params """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'state', 'components', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm state components [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "bulkEnabled",
        "bulkFlagOnly",
        "bulkNID",
        "bulkRole",
        "bulkSoftwareStatus",
        "bulkStateData",
        "byNID",
        "enabled",
        "flagOnly",
        "nID",
        "query",
        "role",
        "softwareStatus",
        "stateData",
        "Commands:",
        "clear",
        "create",
        "delete",
        "describe",
        "list",
        "replace"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_state_components_describe(cli_runner, rest_mock):
    """ Test `cray hsm state components describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components'
    comp = 'x0c0s1b0n0'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'describe', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

def test_cray_hsm_state_components_list(cli_runner, rest_mock):
    """ Test `cray hsm state components list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_state_components_delete(cli_runner, rest_mock):
    """ Test `cray hsm state components delete` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components'
    comp = 'x0c0s1b0n0'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'delete', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

def test_cray_hsm_state_components_clear(cli_runner, rest_mock):
    """ Test `cray hsm state components clear` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'clear', '-y'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_state_components_bynid_describe(cli_runner, rest_mock):
    """ Test `cray hsm state components byNID describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/ByNID'
    nid = '3'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'byNID', 'describe', nid])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, nid)

def test_cray_hsm_state_components_bynid_query_create(cli_runner, rest_mock):
    """ Test `cray hsm state components byNID query create` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/ByNID/Query'
    nid_ranges = '0-24,60-80'
    part = "p1.2"
    stateOnly = True
    flagOnly = True
    roleOnly = True
    nidOnly = True
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'byNID', 'query', 'create',
                                 '--nid-ranges', nid_ranges,
                                 '--partition', part,
                                 '--stateonly', stateOnly,
                                 '--flagonly', flagOnly,
                                 '--roleonly', roleOnly,
                                 '--nidonly', nidOnly])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
        'NIDRanges': nid_ranges.split(','),
        'partition': part,
        'stateonly': stateOnly,
        'flagonly': flagOnly,
        'roleonly': roleOnly,
        'nidonly': nidOnly,
    }

def test_cray_hsm_state_components_bulk_enabled_update(cli_runner, rest_mock):
    """ Test `cray hsm state components bulkEnabled update` with valid params """
    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/BulkEnabled'
    ids = ['x0c0s0b0n0', 'x0c0s1b0n0']
    enabled = True
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'bulkEnabled', 'update',
                                 '--component-ids', ','.join(ids),
                                 '--enabled', enabled])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
       'ComponentIDs': [
            'x0c0s0b0n0', 'x0c0s1b0n0'
        ],
        'Enabled': enabled
    }

def test_cray_hsm_state_components_bulk_flag_only_update(cli_runner, rest_mock):
    """ Test `cray hsm state components bulkFlagOnly update` with valid params """
    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/BulkFlagOnly'
    ids = ['x0c0s0b0n0', 'x0c0s1b0n0']
    flag = 'OK'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'bulkFlagOnly', 'update',
                                 '--component-ids', ','.join(ids),
                                 '--flag', flag])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
       'ComponentIDs': [
            'x0c0s0b0n0', 'x0c0s1b0n0'
        ],
        'Flag': flag
    }

def test_cray_hsm_state_components_bulk_nid_update(cli_runner, rest_mock):
    """ Test `cray hsm state components bulkNID update` with valid params """
    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/BulkNID'
    components_id = ['x0c0s0b0n0', 'x0c0s1b0n0']
    components_nid = ['0','1']
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'bulkNID', 'update',
                                 '--components--id', ','.join(components_id),
                                 '--components--nid', ','.join(components_nid)])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
        'Components': [
            {
                'ID': components_id[0],
                'NID': int(components_nid[0]),
            },
            {
                'ID': components_id[1],
                'NID': int(components_nid[1]),
            }
        ]
    }

def test_cray_hsm_state_components_bulk_role_update(cli_runner, rest_mock):
    """ Test `cray hsm state components bulkRole update` with valid params """
    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/BulkRole'
    ids = ['x0c0s0b0n0', 'x0c0s1b0n0']
    role = 'Compute'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'bulkRole', 'update',
                                 '--component-ids', ','.join(ids),
                                 '--role', role])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
       'ComponentIDs': [
            'x0c0s0b0n0', 'x0c0s1b0n0'
        ],
        'Role': role
    }

def test_cray_hsm_state_components_bulk_software_status_update(cli_runner, rest_mock):
    """ Test `cray hsm state components bulkSoftwareStatus update` with valid params """
    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/BulkSoftwareStatus'
    ids = ['x0c0s0b0n0', 'x0c0s1b0n0']
    status = 'READY'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'bulkSoftwareStatus', 'update',
                                 '--component-ids', ','.join(ids),
                                 '--software-status', status])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
       'ComponentIDs': [
            'x0c0s0b0n0', 'x0c0s1b0n0'
        ],
        'SoftwareStatus': status
    }

def test_cray_hsm_state_components_bulk_state_data_update(cli_runner, rest_mock):
    """ Test `cray hsm state components bulkStateData update` with valid params """
    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/State/Components/BulkStateData'
    ids = ['x0c0s0b0n0', 'x0c0s1b0n0']
    state = 'Ready'
    result = runner.invoke(cli, ['hsm', 'state', 'components', 'bulkStateData', 'update',
                                 '--component-ids', ','.join(ids),
                                 '--state', state])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
       'ComponentIDs': [
            'x0c0s0b0n0', 'x0c0s1b0n0'
        ],
        'State': state
    }

def test_cray_hsm_defaults_nodemaps_create(cli_runner, rest_mock):
    """ Test `cray hsm defaults nodeMaps create` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'defaults', 'nodeMaps', 'create'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm defaults nodeMaps create [OPTIONS]",
        "Options:",
        "--node-maps--sub-role",
        "--node-maps--role",
        "--node-maps--nid",
        "--node-maps--id"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_defaults_nodemaps_create_help(cli_runner, rest_mock):
    """ Test `cray hsm defaults nodeMaps create --help` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'defaults', 'nodeMaps', 'create', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm defaults nodeMaps create [OPTIONS]",
        "Options:",
        "--node-maps--sub-role",
        "--node-maps--role",
        "--node-maps--nid",
        "--node-maps--id"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_defaults_nodemaps_create(cli_runner, rest_mock):
    """ Test `cray hsm defaults nodeMaps create` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Defaults/NodeMaps'
    ids = ['x0c0s0b0n0', 'x0c0s1b0n0']
    nids = ['1', '2']
    roles = ['Service', 'Compute']
    result = runner.invoke(cli, ['hsm', 'defaults', 'nodeMaps', 'create',
                                 '--node-maps--id', ','.join(ids),
                                 '--node-maps--nid', ','.join(nids),
                                 '--node-maps--role', ','.join(roles)])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
        'NodeMaps': [{
            'ID': ids[0],
            'NID': int(nids[0]),
            'Role': roles[0],
        }, {
            'ID': ids[1],
            'NID': int(nids[1]),
            'Role': roles[1],
        }]
    }

def test_cray_hsm_defaults_nodemaps_delete(cli_runner, rest_mock):
    """ Test `cray hsm defaults nodeMaps delete` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Defaults/NodeMaps'
    comp = 'x0c0s1b0n0'
    result = runner.invoke(cli, ['hsm', 'defaults', 'nodeMaps', 'delete', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

def test_cray_hsm_defaults_nodemaps_describe(cli_runner, rest_mock):
    """ Test `cray hsm defaults nodeMaps describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Defaults/NodeMaps'
    comp = 'x0c0s1b0n0'
    result = runner.invoke(cli, ['hsm', 'defaults', 'nodeMaps', 'describe', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

def test_cray_hsm_defaults_nodemaps_list(cli_runner, rest_mock):
    """ Test `cray hsm defaults nodeMaps list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Defaults/NodeMaps'
    result = runner.invoke(cli, ['hsm', 'defaults', 'nodeMaps', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_defaults_nodemaps_replace(cli_runner, rest_mock):
    """ Test `cray hsm defaults nodeMaps replace` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Defaults/NodeMaps'
    comp = 'x0c0s1b0n0'
    nid = 2
    role = 'Compute'
    result = runner.invoke(cli, ['hsm', 'defaults', 'nodeMaps', 'replace',
                                 '--role', role,
                                 '--nid', nid,
                                 comp])
    print(result.output)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)
    assert data['body'] == {
        'NID': nid,
        'Role': role,
    }

def test_cray_hsm_inventory(cli_runner, rest_mock):
    """ Test `cray hsm inventory` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'inventory'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm inventory [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "componentEndpoints",
        "discover",
        "discoveryStatus",
        "ethernetInterfaces",
        "hardware",
        "hardwareByFRU",
        "redfishEndpoints",
        "serviceEndpoints"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_inventory_help(cli_runner, rest_mock):
    """ Test `cray hsm inventory --help` to make sure the expected commands are available """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'inventory', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm inventory [OPTIONS] COMMAND [ARGS]...",
        "Groups:",
        "componentEndpoints",
        "discover",
        "discoveryStatus",
        "ethernetInterfaces",
        "hardware",
        "hardwareByFRU",
        "redfishEndpoints",
        "serviceEndpoints"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_inventory_ethernetinterfaces_clear(cli_runner, rest_mock):
    """ Test `cray hsm inventory ethernetInterfaces clear` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Inventory/EthernetInterfaces'
    result = runner.invoke(cli, ['hsm', 'inventory', 'ethernetInterfaces', 'clear', '-y'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_inventory_ethernetinterfaces_create(cli_runner, rest_mock):
    """ Test `cray hsm inventory ethernetInterfaces create` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Inventory/EthernetInterfaces'
    ip_address = ''
    mac_address = 'ff:ff:ff:ff:ff:ff'
    description = 'Fake Ethernet Interface'
    result = runner.invoke(cli, ['hsm', 'inventory', 'ethernetInterfaces', 'create',
                                 '--ip-address', ip_address,
                                 '--mac-address', mac_address,
                                 '--description', description])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)
    assert data['body'] == {
        'IPAddress': ip_address,
        'MACAddress': mac_address,
        'Description': description
    }

def test_cray_hsm_inventory_ethernetinterfaces_delete(cli_runner, rest_mock):
    """ Test `cray hsm inventory ethernetInterfaces delete` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Inventory/EthernetInterfaces'
    ethinterface_id = 'ffffffffffff'
    result = runner.invoke(cli, ['hsm', 'inventory', 'ethernetInterfaces', 'delete', ethinterface_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, ethinterface_id)

def test_cray_hsm_inventory_ethernetinterfaces_describe(cli_runner, rest_mock):
    """ Test `cray hsm inventory ethernetInterfaces describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Inventory/EthernetInterfaces'
    ethinterface_id = 'ffffffffffff'
    result = runner.invoke(cli, ['hsm', 'inventory', 'ethernetInterfaces', 'describe', ethinterface_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, ethinterface_id)

def test_cray_hsm_inventory_ethernetinterfaces_list(cli_runner, rest_mock):
    """ Test `cray hsm inventory ethernetInterfaces list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Inventory/EthernetInterfaces'
    result = runner.invoke(cli, ['hsm', 'inventory', 'ethernetInterfaces', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_inventory_ethernetinterfaces_update(cli_runner, rest_mock):
    """ Test `cray hsm inventory ethernetInterfaces update` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/Inventory/EthernetInterfaces'
    ethinterface_id = 'ffffffffffff'
    ip_address = ''
    description = 'Fake Ethernet Interface 2'
    result = runner.invoke(cli, ['hsm', 'inventory', 'ethernetInterfaces', 'update',
                                 '--ip-address', ip_address,
                                 '--description', description, ethinterface_id])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, ethinterface_id)
    assert data['body'] == {
        'IPAddress': ip_address,
        'Description': description
    }

def test_cray_hsm_groups_describe(cli_runner, rest_mock):
    """ Test `cray hsm groups describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/groups'
    label = 'blue'
    result = runner.invoke(cli, ['hsm', 'groups', 'describe', label])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, label)

def test_cray_hsm_groups_list(cli_runner, rest_mock):
    """ Test `cray hsm groups list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/groups'
    result = runner.invoke(cli, ['hsm', 'groups', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_group_members_list(cli_runner, rest_mock):
    """ Test `cray hsm group members list` with valid params """

    runner, cli, config = cli_runner
    url_template1 = '/apis/smd/hsm/v1/groups'
    url_template2 = 'members'
    label = 'blue'
    result = runner.invoke(cli, ['hsm', 'groups', 'members', 'list', '--partition', 'part1', label])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}/{}?{}'.format(config['default']['hostname'],
                                                 url_template1, label, url_template2,
                                                 'partition=part1')

def test_cray_hsm_group_members_create(cli_runner, rest_mock):
    """ Test `cray hsm groups members create blue` with valid params """

    runner, cli, config = cli_runner
    url_template1 = '/apis/smd/hsm/v1/groups'
    url_template2 = 'members'
    label = 'blue'
    comp = 'x0c0s0b0n0'
    result = runner.invoke(cli, ['hsm', 'groups', 'members', 'create', label,
                                 '--id', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}/{}/{}'.format(config['default']['hostname'],
                                              url_template1, label, url_template2)
    assert data['body'] == {
        'id': comp,
    }

def test_cray_hsm_group_members_delete(cli_runner, rest_mock):
    """ Test `cray hsm groups members delete xname blue` with valid params """

    runner, cli, config = cli_runner
    url_template1 = '/apis/smd/hsm/v1/groups'
    url_template2 = 'members'
    label = 'blue'
    comp = 'x0c0s0b0n0'
    result = runner.invoke(cli, ['hsm', 'groups', 'members', 'delete', comp, label])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}{}/{}/{}/{}'.format(config['default']['hostname'],
                                                 url_template1, label,
                                                 url_template2, comp)

def test_cray_hsm_partitions_describe(cli_runner, rest_mock):
    """ Test `cray hsm partitions describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/partitions'
    pname = 'part1'
    result = runner.invoke(cli, ['hsm', 'partitions', 'describe', pname])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, pname)

def test_cray_hsm_partitions_list(cli_runner, rest_mock):
    """ Test `cray hsm partitions list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/partitions'
    result = runner.invoke(cli, ['hsm', 'partitions', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_partition_members_list(cli_runner, rest_mock):
    """ Test `cray hsm partition members list` with valid params """

    runner, cli, config = cli_runner
    url_template1 = '/apis/smd/hsm/v1/partitions'
    url_template2 = 'members'
    pname = 'part1'
    result = runner.invoke(cli, ['hsm', 'partitions', 'members', 'list', pname])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}/{}'.format(config['default']['hostname'],
                                              url_template1, pname, url_template2)

def test_cray_hsm_partition_members_create(cli_runner, rest_mock):
    """ Test `cray hsm partitions members create blue` with valid params """

    runner, cli, config = cli_runner
    url_template1 = '/apis/smd/hsm/v1/partitions'
    url_template2 = 'members'
    pname = 'part1'
    comp = 'x0c0s0b0n0'
    result = runner.invoke(cli, ['hsm', 'partitions', 'members', 'create', pname,
                                 '--id', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}{}/{}/{}'.format(config['default']['hostname'],
                                              url_template1, pname, url_template2)
    assert data['body'] == {
        'id': comp,
    }

def test_cray_hsm_memberships_describe(cli_runner, rest_mock):
    """ Test `cray hsm memberships describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/memberships'
    comp = 'x0c0s0b0n0'
    result = runner.invoke(cli, ['hsm', 'memberships', 'describe', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

def test_cray_hsm_memberships_list(cli_runner, rest_mock):
    """ Test `cray hsm memberships list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/memberships'
    result = runner.invoke(cli, ['hsm', 'memberships', 'list', '--type', 'node', '--group', 'blue'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}?{}'.format(config['default']['hostname'],
                                           url_template, 'type=node&group=blue')

def test_cray_hsm_locks(cli_runner, rest_mock):
    """ Test `cray hsm locks` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'locks'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm locks [OPTIONS] COMMAND [ARGS]...",
        "Commands:",
        "delete",
        "describe",
        "list"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_locks_help(cli_runner, rest_mock):
    """ Test `cray hsm locks --help` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'locks', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm locks [OPTIONS] COMMAND [ARGS]...",
        "Commands:",
        "delete",
        "describe",
        "list"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_locks_list_help(cli_runner, rest_mock):
    """ Test `cray hsm locks list --help` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'locks', 'list', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm locks list [OPTIONS]",
        "Options:",
        "--xname",
        "--owner",
        "--id"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_locks_list(cli_runner, rest_mock):
    """ Test `cray hsm locks list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/locks'
    owner = 'me'
    lock = 'bf9362ad-b29c-40ed-9881-18a5dba3a26b'
    comp = 'x0c0s1b0n0'
    result = runner.invoke(cli, ['hsm', 'locks', 'list', '--owner', owner,
                                 '--id', lock, '--xname', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}?{}{}&{}{}&{}{}'.format(config['default']['hostname'],
                                                       url_template,
                                                       'owner=', owner,
                                                       'xname=', comp,
                                                       'id=', lock,)

def test_cray_hsm_locks_describe(cli_runner, rest_mock):
    """ Test `cray hsm locks describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/locks'
    lock = 'bf9362ad-b29c-40ed-9881-18a5dba3a26b'
    result = runner.invoke(cli, ['hsm', 'locks', 'describe', lock])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, lock)

def test_cray_hsm_sysinfo_powermaps(cli_runner, rest_mock):
    """ Test `cray hsm sysinfo powermaps` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'sysinfo', 'powermaps'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm sysinfo powermaps [OPTIONS] COMMAND [ARGS]...",
        "Commands:",
        "create",
        "delete",
        "describe",
        "list",
        "replace"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_sysinfo_powermaps_help(cli_runner, rest_mock):
    """ Test `cray hsm sysinfo powermaps --help` """

    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['hsm', 'sysinfo', 'powermaps', '--help'])
    assert result.exit_code == 0
    outputs = [
        "cli hsm sysinfo powermaps [OPTIONS] COMMAND [ARGS]...",
        "Commands:",
        "create",
        "delete",
        "describe",
        "list",
        "replace"
    ]
    for out in outputs:
        assert out in result.output

def test_cray_hsm_sysinfo_powermaps_delete(cli_runner, rest_mock):
    """ Test `cray hsm sysinfo powermaps delete` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/sysinfo/powermaps'
    comp = 'x0c0s1b0n0'
    result = runner.invoke(cli, ['hsm', 'sysinfo', 'powermaps', 'delete', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

def test_cray_hsm_sysinfo_powermaps_describe(cli_runner, rest_mock):
    """ Test `cray hsm sysinfo powermaps describe` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/sysinfo/powermaps'
    comp = 'x0c0s1b0n0'
    result = runner.invoke(cli, ['hsm', 'sysinfo', 'powermaps', 'describe', comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)

def test_cray_hsm_sysinfo_powermaps_list(cli_runner, rest_mock):
    """ Test `cray hsm sysinfo powermaps list` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/sysinfo/powermaps'
    result = runner.invoke(cli, ['hsm', 'sysinfo', 'powermaps', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}{}'.format(config['default']['hostname'], url_template)

def test_cray_hsm_sysinfo_powermaps_replace(cli_runner, rest_mock):
    """ Test `cray hsm sysinfo powermaps replace` with valid params """

    runner, cli, config = cli_runner
    url_template = '/apis/smd/hsm/v1/sysinfo/powermaps'
    comp = 'x0c0s1b0n0'
    poweredby = ['x0m0j0', 'x0m0j1']
    result = runner.invoke(cli, ['hsm', 'sysinfo', 'powermaps', 'replace',
                                 '--powered-by', ','.join(poweredby), comp])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PUT'
    assert data['url'] == '{}{}/{}'.format(config['default']['hostname'], url_template, comp)
    assert data['body'] == {
        'poweredBy': poweredby
    }
