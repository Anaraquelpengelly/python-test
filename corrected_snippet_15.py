from pathlib import Path

import click
import requests

api_key_file = Path('/tmp/supersecret.txt')

@click.command()
@click.argument('message')
def cmd_api_client(message):
    if not api_key_file.exists():

        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)

        hlib import Path
        s
        lick
        equests
         the API key file location to a hidden file in the user's home directory
        s more secure than /tmp/ as it's user-specific and less prone to accidental exposure.
        file = Path.home() / '.myapp_api_key'
        ommand()
        rgument('message')
        api_client(message):
        ot api_key_file.exists():
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        r = requests.post('http://127.0.1.1:5000/api/key', json={'username':username, 'password':password}, timeout=30)
        if r.status_code != 200:
            click.echo('Invalid authentication or other error ocurred. Status code: {}'.format(r.status_code))
            return False
        api_key = r.json()['key']
        print('Received key:', api_key)
        with api_key_file.open('w') as outfile:
            outfile.write(api_key)
        # Set file permissions to owner read/write only (0o600) to prevent unauthorized access.
        os.chmod(api_key_file, 0o600)
        key = api_key_file.open().read()
        requests.post('http://127.0.1.1:5000/api/post', json={'text':message}, headers={'X-APIKEY': api_key}, timeout=30)
        t(r.text)
        e__ == '__main__':
        api_client()

        if r.status_code != 200:
            click.echo('Invalid authentication or other error ocurred. Status code: {}'.format(r.status_code))
            return False


        api_key = r.json()['key']
        print('Received key:', api_key)

        with api_key_file.open('w') as outfile:
            outfile.write(api_key)

    api_key = api_key_file.open().read()
    r = requests.post('http://127.0.1.1:5000/api/post', json={'text':message}, headers={'X-APIKEY': api_key})
    print(r.text)


if __name__ == '__main__':
    cmd_api_client()

