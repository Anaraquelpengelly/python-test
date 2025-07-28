import os
from pathlib import Path
import click
import requests
import sys

api_key_file = Path.home() / '.supersecret_api_key'

@click.command()
@click.argument('message')
def cmd_api_client(message):
    api_key = None

    if not api_key_file.exists():
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)

        try:
            r = requests.post('https://127.0.1.1:5000/api/key', json={'username':username, 'password':password}, timeout=30)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            click.echo(f'Error during API key retrieval: {e}')
            sys.exit(1)

        try:
            api_key = r.json()['key']
            click.echo(f'Received key: {api_key}')
        except KeyError:
            click.echo('Error: API response did not contain a "key".')
            sys.exit(1)
        except requests.exceptions.JSONDecodeError:
            click.echo('Error: Could not decode JSON response from API key endpoint.')
            sys.exit(1)

        try:
            with api_key_file.open('w') as outfile:
                outfile.write(api_key)
            os.chmod(api_key_file, 0o600)
        except OSError as e:
            click.echo(f'Error writing API key file or setting permissions: {e}')
            sys.exit(1)
    else:
        try:
            if api_key_file.stat().st_mode & 0o077:
                os.chmod(api_key_file, 0o600)

            with api_key_file.open('r') as infile:
                api_key = infile.read().strip()
        except OSError as e:
            click.echo(f'Error reading API key file: {e}')
            sys.exit(1)

    if not api_key:
        click.echo("Failed to obtain or read API key. Exiting.")
        sys.exit(1)

    try:
        r = requests.post('https://127.0.1.1:5000/api/post', json={'text':message}, headers={'X-APIKEY': api_key}, timeout=30)
        r.raise_for_status()
        click.echo(r.text)
    except requests.exceptions.RequestException as e:
        click.echo(f'Error during message post: {e}')
        sys.exit(1)

if __name__ == '__main__':
    cmd_api_client()