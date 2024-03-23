ssh bruteforce and scanning tool

# description

use this tool to scan a large number of hosts for running ssh services and then bruteforce these services with specified lists of logins and passwords

the logic of the tool's operation consists of two modes:
1. scan: the tool, using the specified list of ip addresses or domain names of hosts, sends connection requests and, receiving any response from them, gradually adds them to the lists of active hosts, thus allowing to understand which hosts among others are really worth to brute force
2. brute: the tool, using a list of active hosts, as well as lists with logins and passwords, starts testing hosts in batches, allowing you to monitor this process in real time.
you can perform them either sequentially or individually

# preparation

to make the tool work, you need to perform a number of preliminary actions
first, use the "make" utility and execute "make prepare" to install the main libraries and "make create_env" to create a local file with environment variables
if the "make" utility is not available or cannot be installed, you can run the commands specified in "MakeFile" yourself

next, you need to create several files, namely:
1. a file that will contain ip addresses or domain names of hosts
2. a file that will contain logins
3. a file that will contain passwords
the directory where these files should be located (by default it is data/), as well as their names, you can find out and change in the environment variables file you created in the previous step

# usage

usage: ssh_brute [-h] [-v] -i IP_FILE -l LOGINS_FILE -p PASSWORDS_FILE -m MODE

options:
  -h, --help            show this help message and exit
  -v, --version         show the version of this program and exit
  -i IP_FILE, --ip_file IP_FILE
                        name of the file with ip addresses or domain names
  -l LOGINS_FILE, --logins_file LOGINS_FILE
                        name of the file with ip addresses or domain names
  -p PASSWORDS_FILE, --passwords_file PASSWORDS_FILE
                        name of the file with ip addresses or domain names
  -m MODE, --mode MODE  script mode (scan, brute, all)
