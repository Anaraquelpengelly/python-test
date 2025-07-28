from pathlib import Path
import click
import requests
import os

api_key_dir = Path.home() / '.config' / 'myapp'
api_key_file = api_key_dir / 'api_key.txt'

@click.command()
@click.argument('message')
def cmd_api_client(message):
    api_key_dir.mkdir(parents=True, exist_ok=True)

    if not api_key_file.exists():
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)

        try:
            r = requests.post('https://127.0.1.1:5000/api/key', json={'username':username, 'password':password}, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            click.echo('Error during authentication request: {}'.format(e))
            return False

        try:
            api_key = r.json()['key']
        except (KeyError, requests.exceptions.JSONDecodeError):
            click.echo('Failed to parse API key from response.')
            return False

        print('Received key:', api_key)

        try:
            with api_key_file.open('w') as outfile:
                outfile.write(api_key)
            os.chmod(api_key_file, 0o600)
        except OSError as e:
            click.echo('Error writing API key file: {}'.format(e))
            return False

    try:
        with api_key_file.open('r') as infile:
            api_key = infile.read().strip()
    except OSError as e:
        click.echo('Error reading API key file: {}'.format(e))
        return False

    if not api_key:
        click.echo('API key is empty or could not be read.')
        return False

    try:
        r = requests.post('https://127.0.1.1:5000/api/post', json={'text':message}, headers={'X-APIKEY': api_key}, timeout=30)
        r.raise_for_status()
        print(r.text)
    except requests.exceptions.RequestException as e:
        click.echo('Error during post request: {}'.format(e))
        return False

if __name__ == '__main__':
    cmd_api_client()