import click
import requests

@click.group(name="rr", help="Rack Resiliency commands")
def cli():
    pass

# Existing list command
@cli.command(name="list", help="List rack resiliency information")
def list_command():
    click.echo("Hello World in the terminal")

@cli.command(name="hello", help="Fetch greeting from HelloWorld API")
@click.option('--name', '-n', default=None, help="Name for personalized greeting")
@click.option('--external-ip', '-e', required=True, 
             help="External IP of HelloWorld service (port 8080)")
def hello_command(name, external_ip):
    """Fetch greeting from /hello endpoint"""
    base_url = f"http://{external_ip}:8080"
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