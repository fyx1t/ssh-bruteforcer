from scripts.helpers import get_ips, check_for_good_ips
from termcolor import colored
import os

def start(env, arguments):
    ips = get_ips(env, arguments)
    good_ips = check_for_good_ips(ips, env)
    print('[INFO] SAVING TO FILE...')
    good_ips_filename: dict = env['FILENAME_GOOD_IPS']
    os.system(f'rm -f {good_ips_filename}')
    with open(f'{env["OUTPUT_FOLDER"]}{good_ips_filename}', 'w') as good_ips_file:
        for ip in good_ips:
            good_ips_file.write(ip + '\n')
    print('[INFO] SCAN FINISHED')


if __name__ == '__main__':
    print(colored('[WARNING] PLEASE LAUNCH ssh_brute.py', 'red'))
