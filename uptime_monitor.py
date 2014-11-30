import os, logging, requests, datetime

#Configure Logging
logging.basicConfig(filename='output.log', level=logging.DEBUG)
logging.info('Started')

hostsfile = 'hosts.cfg'

# Check if users file exists, if not throw error
def hostLoad(hostsfile):
    if os.path.isfile(hostsfile):
        logging.info('Reading hosts from %s', hostsfile)
        hostlist = [line.strip() for line in open(hostsfile)]
        logging.debug('Hosts: %s', hostlist)
        return(hostlist)
    else:
        logging.error("Cannot find file specified, please try again.", exc_info=True)

def hostCheck(hostlist):
    for host in hostlist:
        check = requests.get(host)
        hostcode = check.status_code
        if hostcode == 200:
            logging.info("{} {} returned status code {}".format(datetime.datetime.now(),host,hostcode))
        else:
            logging.info("{} ERROR! {} returned status code {}".format(datetime.datetime.now(),host,hostcode))

hostlist = hostLoad(hostsfile)
hostCheck(hostlist)
