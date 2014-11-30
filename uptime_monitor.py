import os, sys, logging, configparser, requests, datetime, smtplib

#Configure Logging
logging.basicConfig(filename='output.log', level=logging.DEBUG)
logging.info('Started')
#Load config.ini
parser = configparser.ConfigParser() 
parser.read('config.ini')
#Server to check
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

def notify(input_message,host):
    mail_to = parser.get('NOTIFY','mail_to')
    mail_from = parser.get('NOTIFY','mail_from')
    mail_user = parser.get('NOTIFY','mail_user')
    mail_pwd = parser.get('NOTIFY','mail_pwd')
    mail_server = parser.get('NOTIFY','mail_server')
    smtpserver = smtplib.SMTP(mail_server,25)
    smtpserver.ehlo()
    #smtpserver.starttls()
    smtpserver.ehlo
    #smtpserver.login(mail_user,mail_pwd)
    header = "To: {}\nFrom:{}\nSubject:DOWN {}\n".format(mail_to,mail_from,host)
    input_message = input_message + host
    message = header + input_message
    smtpserver.sendmail(mail_user, mail_to, message)
    smtpserver.close

def hostCheck(hostlist):
    for host in hostlist:
        try:
            check = requests.get(host)
            hostcode = check.status_code
        except:
            hostcode = sys.exc_info()[0]
        if hostcode == requests.codes.ok:
            logging.info("{} {} returned status code {}".format(datetime.datetime.now(),host,hostcode))
            return("up")
        else:
            return(hostError(host, hostcode))

def hostError(host, hostcode):
    host_error = ("{} ERROR! {} returned status code {}".format(datetime.datetime.now(),host,hostcode))
    logging.info(host_error)
    notify(host_error,host)
    return("down")

hostlist = hostLoad(hostsfile)
print(hostCheck(hostlist))
