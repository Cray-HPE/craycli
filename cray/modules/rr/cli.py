import click
import requests
import subprocess
import json
from collections import defaultdict

@click.group(name="rr", help="Rack Resiliency commands")
def cli():
    pass
# cray/modules/rr/cli.py

# def get_zone_data():
#     """Fetch and parse Kubernetes node zone information"""
#     try:
#         # Get node data with zone labels and resources
#         cmd = [
#             'kubectl', 'get', 'nodes',
#             '-L', 'topology.kubernetes.io/zone',
#             '-o', 'json'
#         ]
#         result = subprocess.check_output(cmd, text=True)
#         data = json.loads(result)
        
#         # Organize nodes by zone
#         zones = defaultdict(list)
#         for node in data['items']:
#             zone = node['metadata']['labels'].get(
#                 'topology.kubernetes.io/zone', 
#                 'unassigned'
#             )
#             zones[zone].append({
#                 'name': node['metadata']['name'],
#                 'status': node['status'].get('conditions', [{}])[-1].get('type', 'Unknown'),
#                 'roles': ','.join(
#                     k for k, v in node['metadata']['labels'].items()
#                     if 'node-role.kubernetes.io/' in k
#                 ),
#                 'age': node['metadata']['creationTimestamp'],
#                 'version': node['status']['nodeInfo']['kubeletVersion'],
#                 'cpu': node['status']['capacity'].get('cpu', 'N/A'),
#                 'memory': node['status']['capacity'].get('memory', 'N/A')
#             })
#         return zones
        
#     except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
#         click.echo(f"Error fetching node data: {str(e)}", err=True)
#         return {}

@cli.command(name="list", help="List nodes grouped by zones from backend API")
@click.option('--node-ip', '-e', required=True, 
             help="node IP of the backend service")
def list_command(node_ip):
    """Display nodes organized by zone with resource information"""
    try:
        # Fetch data from backend API
        response = requests.get(f"http://{node_ip}:8080/zones")  # Update endpoint if needed
        print(response)
        response.raise_for_status()
        zones_data = response.json()
        
        # Formatting constants
        header = "{:<10} {:<8} {:<18} {:<10} {:<12} {:<6} {:<15}".format(
            "NAME", "STATUS", "ROLES", "AGE", "VERSION", "CPU", "MEMORY"
        )
        separator = "-" * 85
        
        for zone, nodes in zones_data.items():
            click.echo(f"\nZone: {zone}")
            click.echo(separator)
            click.echo(header)
            
            for node in nodes:
                # Clean up role display
                roles = node['roles'].split('/')[-1] if node['roles'] else 'worker'
                
                # Format age without timestamp
                age = node['age'].split('T')[0] if 'T' in node['age'] else node['age']
                
                click.echo(
                    "{name:<10} {status:<8} {roles:<18} {age:<10} "
                    "{version:<12} {cpu:<6} {memory:<15}".format(
                        name=node['name'],
                        status=node['status'],
                        roles=roles,
                        age=age,
                        version=node['version'],
                        cpu=node['cpu'],
                        memory=node['memory']
                    )
                )
            click.echo()
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error connecting to backend: {str(e)}", err=True)
    except KeyError as e:
        click.echo(f"Invalid data format from backend: missing {str(e)}", err=True)


# @cli.command(name="list", help="List nodes grouped by zones")
# def list_command():
#     """Display nodes organized by zone with resource information"""
#     zones = get_zone_data()
    
#     # Formatting constants
#     header = "{:<15} {:<10} {:<25} {:<10} {:<15} {:<10} {:<15}".format(
#         "NAME", "STATUS", "ROLES", "AGE", "VERSION", "CPU", "MEMORY"
#     )
#     separator = "-" * 100
    
#     for zone, nodes in zones.items():
#         click.echo(f"\nZone: {zone}")
#         click.echo(separator)
#         click.echo(header)
        
#         for node in nodes:
#             click.echo(
#                 "{name:<15} {status:<10} {roles:<25} {age:<10} "
#                 "{version:<15} {cpu:<10} {memory:<15}".format(
#                     name=node['name'],
#                     status=node['status'],
#                     roles=node['roles'][:23] + '..' if len(node['roles']) > 25 else node['roles'],
#                     age=node['age'].split('T')[0],  # Show date only
#                     version=node['version'],
#                     cpu=node['cpu'],
#                     memory=node['memory']
#                 )
#             )
#         click.echo()  # Add space between zones

@cli.command(name="hello", help="Fetch greeting from HelloWorld API")
@click.option('--name', '-n', default=None, help="Name for personalized greeting")
@click.option('--node-ip', '-e', required=True, help="Node IP of HelloWorld service (port 8080)")
def hello_command(name, node_ip):
    """Fetch greeting from /hello endpoint"""
    base_url = f"http://{node_ip}:8080"
    endpoint = f"{base_url}/hello"
    try:
        response = requests.get(
            endpoint,
            params={'name': name} if name else None,
            timeout=5  # Add timeout
        )
        response.raise_for_status()
        # Add JSON parsing validation
        try:
            data = response.json()
            click.echo(f"Response: {data['message']}")
        except ValueError:
            click.echo(f"Invalid JSON response. Raw response: {response.text}", err=True) 
    except requests.exceptions.HTTPError as e:
        click.echo(f"HTTP Error {e.response.status_code}: {e.response.text}", err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f"Connection Error: {str(e)}", err=True)
