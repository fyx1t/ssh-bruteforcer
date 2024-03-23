touch .env

echo -e "ALLOW_COMMANDS=true\nCOMMANDS=hostname, ip a\nTHREADS=8\nENTER_TO_CONTINUE=false\nFILENAME_GOOD_IPS=good_ips.txt\nFILENAME_ERRORS=errors.txt\nFILENAME_FOUND_IPS=found.txt\nFILENAME_FOUND_IPS_EXTENDED=found_extended.txt\nFILENAME_LOGS=work.log\nINPUT_FOLDER=data/\nOUTPUT_FOLDER=data/\nVERSION=v0.2" > .env
