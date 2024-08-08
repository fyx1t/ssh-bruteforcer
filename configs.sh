touch .env

echo -e "PORT=22\nALLOW_COMMANDS=true\nCOMMANDS=hostname, ip a\nTHREADS=20\nENTER_TO_CONTINUE=false\nTIMEOUT=2\nFILENAME_GOOD_IPS=good_ips.txt\nFILENAME_ERRORS=errors.txt\nFILENAME_FOUND_IPS=found.txt\nFILENAME_FOUND_IPS_EXTENDED=found_extended.txt\nFILENAME_LOGS=work.log\nOUTPUT_FOLDER=results/\nVERSION=v0.4" > .env
