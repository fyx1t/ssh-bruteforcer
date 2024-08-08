from scripts.helpers import get_ips, check_for_good_ips, check_for_good_ips, Threads
import os

def start(env, arguments):
    threads = Threads(env['THREADS'])
    ips = get_ips(env, arguments)

    jobs_resources = [[] for i in range(env["THREADS"])]

    job_resource_id = 0
    for ip in ips:
        if job_resource_id == len(jobs_resources):
            job_resource_id = 0
        jobs_resources[job_resource_id].append(ip)
        job_resource_id += 1

    for i in range(env['THREADS']):
        threads.jobs.append([check_for_good_ips, jobs_resources[i], env])

    os.system(f'rm -f {env["OUTPUT_FOLDER"]}{env["FILENAME_GOOD_IPS"]}')
    threads.run()
    del threads
    print('[INFO] SCAN FINISHED')

if __name__ == '__main__':
    print('[WARNING] PLEASE LAUNCH ssh_brute.py')
