from scripts import brute, scan
from scripts.helpers import get_parser
from configs.exceptions import ArgumentBadValueError, NoKeyError
from dotenv import dotenv_values
import os
import time

def phase_1(env, arguments):
    os.system('clear')
    
    print('[SCAN] START SCANNING...\n')
    
    scan.start(env, arguments)
    
def phase_2(env, arguments, only: bool = False):
    os.system('clear')
    
    print('[BRUTE] START BRUTEFORCING...')
    
    brute.start(env, arguments, only)

def main():
    ENV: dict = dotenv_values()
    ENV['THREADS'] = int(ENV['THREADS'])
    
    os.system(f'mkdir {ENV["OUTPUT_FOLDER"]}')

    parser = get_parser(ENV)
    arguments = parser.parse_args()

    timer_1 = time.time()
    
    if arguments.mode == 'scan':
        phase_1(ENV, arguments)
    elif arguments.mode == 'brute':
        if arguments.logins_file and arguments.passwords_file:
            phase_2(ENV, arguments, True)
        else:
            raise NoKeyError()
    elif arguments.mode == 'all':
        if arguments.logins_file and arguments.passwords_file:
            phase_1(ENV, arguments)
            phase_2(ENV, arguments)
        else:
            raise NoKeyError()
    else:
        raise ArgumentBadValueError('-m (--mode)')

    print(f'\nSCRIPT WORKED FOR {time.time() - timer_1} SECONDS')

if __name__ == '__main__':
    main()
