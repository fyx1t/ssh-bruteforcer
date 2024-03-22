ssh bruteforce and scanning tool

usage: ssh_brute [-h] [-v] -i IP_FILE -l LOGINS_FILE -p PASSWORDS_FILE -m MODE

SSH scanning and bruteforce tool

options:
  -h, --help            show this help message and exit
  -v, --version         show the version of this program and exit
  -i IP_FILE, --ip_file IP_FILE
                        name of the file with ip addresses or domain names
  -l LOGINS_FILE, --logins_file LOGINS_FILE
                        name of the file with ip addresses or domain names
  -p PASSWORDS_FILE, --passwords_file PASSWORDS_FILE
                        name of the file with ip addresses or domain names
  -m MODE, --mode MODE  script phase (scan, brute, all)
