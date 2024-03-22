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
        "--ip_list",
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
    with open(f'{env["INPUT_FOLDER"]}{arguments.ip_list}', 'r') as ips_file:
        ips = ips_file.read().split('\n')
    
    for i in range(len(ips)):
        if '_' in ips[i]:
            ips[i] = ips[i].split('_')
            
    return ips

def get_good_ips() -> list:
    pre_ips = []
    with open('good_ips.txt', 'r') as ips_file:
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

def prepare(ENV):
    threads = Threads(ENV['THREADS'])
    print(colored(f'THERE WILL BE {ENV["THREADS"]} THREADS', 'green'))

    LOGINS: list = []
    PASSWORDS: list = []
    with open('logins_to_crack.txt', 'r') as logins_file:
        for line in logins_file:
            LOGINS.append(line.replace('\n', ''))

    with open('passwords_to_crack.txt', 'r') as passwords_file:
        for line in passwords_file:
            PASSWORDS.append(line.replace('\n', ''))

    print(colored('CREDENTIONALS ARE LOADED', 'green'))

    current_work_ips: list = ['' for i in range(ENV['THREADS'])]
    current_creds: list = ['' for i in range(ENV['THREADS'])]
    worked_ips: list = []
    good_ips: list = []
    
    os.system('rm -f found.txt; touch found.txt')
    os.system('rm -f found-extended.txt; touch found-extended.txt')
    os.system('rm -f errors.txt; touch errors.txt')
    
    return LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips

class Threads:
    def __init__(self, count) -> None:
        self.threads: list = []
        self.jobs: list = []
        self.count = count

    def run(self):
        # 1 argument MAX
        for i in range(self.count):
            self.threads.append(
                threading.Thread(target=self.jobs[i][0], args=(self.jobs[i][1], self.jobs[i][2]))
            )
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    print(colored('[WARNING] PLEASE LAUNCH ssh_brute.py', 'red'))
