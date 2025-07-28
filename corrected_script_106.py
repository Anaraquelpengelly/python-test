#!/usr/bin/env python3

import click
import requests
import tempfile

MINLENGTH = 12
URL = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt'


@click.command()
@click.option('-o', 'outfile', default='-', type=click.File('w'), help='Output file (default: stdout)')
@click.option('-u', 'url', default=URL, help='URL to retrieve password file')
@click.option('-l', 'minlength', default=MINLENGTH, help='Minimum password length')
def generate_leaked_passwords(outfile, url, minlength):

    with tempfile.TemporaryFile(mode='w+b') as temp_file:

        click.echo('Downloading password file...', nl=False, err=True)
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    click.echo('.', nl=False, err=True)
                    temp_file.write(chunk)

        click.echo('OK', err=True)
        temp_file.seek(0)

        for line in temp_file:
            password = line.decode('utf-8').strip()

            if not password:
                continue

            if len(password) < minlength:
                continue

            outfile.write(password + '\n')


if __name__ == '__main__':
    generate_leaked_passwords()