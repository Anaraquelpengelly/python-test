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

        r = requests.post('http://127.0.1.1:5000/api/key', json={'username':username, 'password':password})

        if r.status_code != 200:
            click.echo('Invalid authentication or other error ocurred. Status code: {}'.format(r.status_code))
            return False


        api_key = r.json()['key']
        print('Received key:', api_key)

        with api_key_file.open('w') as outfile:
            outfile.write(api_key)

    api_key = api_key_file.open().read()
     pathlib import Path
    rt os
    rt click
    rt requests
    key_file = Path.home() / ".my_app_api_key"
    ck.command()
    ck.argument('message')
    cmd_api_client(message):
    if not api_key_file.exists():
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
        os.chmod(api_key_file, 0o600)
    with api_key_file.open('r') as infile:
        api_key = infile.read().strip()
    r = requests.post('http://127.0.1.1:5000/api/post', json={'text':message}, headers={'X-APIKEY': api_key}, timeout=30)
    print(r.text)
    _name__ == '__main__':
    cmd_api_client()
    print(r.text)


if __name__ == '__main__':
    cmd_api_client()

