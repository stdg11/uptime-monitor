import os, logging, requests

#Configure Logging
logging.basicConfig(filename='output.log', level=logging.DEBUG)
logging.info('Started')

hostsfile = 'hosts.cfg'

# Check if users file exists, if not throw error
if os.path.isfile(hostsfile):
    logging.info('Reading hosts from %s', hostsfile)
    hostlist = [line.strip() for line in open(hostsfile)]
    logging.debug('Hosts: %s', hostlist)
    print(hostlist)
else:
    logging.error("Cannot find file specified, please try again.", exc_info=True)

for host in hostlist:
    check = requests.get(host)
    hostcode = check.status_code
    print("{} returned status code {}".format(host,hostcode))
