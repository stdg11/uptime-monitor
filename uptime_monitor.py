import os, sys, logging, configparser, requests, time, smtplib, datetime
from threading import Thread
#Configure Logging
logging.basicConfig(filename='output.log', level=logging.DEBUG)
logging.info('Started')
#Load config.ini
parser = configparser.ConfigParser() 
parser.read('config.ini')
#Server to check
hostsfile = 'hosts.cfg'
#Downtime hostlist
down_hosts = []

# Check if users file exists, if not throw error
def hostLoad():
    if os.path.isfile(hostsfile):
        logging.info('Reading hosts from %s', hostsfile)
        hostlist = [line.strip() for line in open(hostsfile)]
        logging.debug('Hosts: %s', hostlist)
        return(hostlist)
    else:
        logging.error("Cannot find file specified, please try again.", exc_info=True)

def notify(host, status, error):
    mail_to = parser.get('NOTIFY','mail_to')
    mail_from = parser.get('NOTIFY','mail_from')
    mail_user = parser.get('NOTIFY','mail_user')
    mail_pwd = parser.get('NOTIFY','mail_pwd')
    mail_server = parser.get('NOTIFY','mail_server')
    try:
        smtpserver = smtplib.SMTP(mail_server,25)
        smtpserver.ehlo()
        #smtpserver.starttls()
        smtpserver.ehlo
        #smtpserver.login(mail_user,mail_pwd)
        header = "To: {}\nFrom:{}\nSubject:{} {}\n".format(mail_to,mail_from,status,host)
        input_message = error
        message = header + input_message
        smtpserver.sendmail(mail_user, mail_to, message)
        smtpserver.close
    except:
        smtp_error = ("{} exception {}".format(datetime.datetime.now(),sys.exc_info()[0]))
        logging.error(smtp_error)
        print(smtp_error)

def hostCheck():
    while True:
        for host in hostlist:
            try:
                check = requests.get(host)
                hostcode = check.status_code
                if hostcode == requests.codes.ok:
                    logging.info("{} {} returned status code {}".format(datetime.datetime.now(),host,hostcode))
                    return(host, "Site OK")
                    #time.sleep(60)
                else:
                    error = ("{} ERROR! {} returned status code {}".format(datetime.datetime.now(),host,hostcode))
                    logging.error(error)
                    onError(host,error)
            except:
                error = ("{} {} exception {}".format(datetime.datetime.now(),host,sys.exc_info()[0]))
                logging.error(error)
                onError(host,error)

def onError(host,error):
    down_hosts.append(host)
    hostlist.remove(host)
    logging.info(host, "-Added to Downtime monitor")
    notify(host, "DOWN!", error)
    return(host, "DOWN!")

def hostError():
    while True:
        #time.sleep(120)
        for host in down_hosts:
            try:
                check = requests.get(host)
                hostcode = check.status_code
                if hostcode == requests.codes.ok:
                    error = ("{} {} Site back UP!".format(datetime.datetime.now(),host))
                    logging.info(error)
                    hostlist.append(host)
                    down_hosts.remove(host)
                    notify(host,"UP!",error)
                else:
                    print("{} Still DOWN!".format(host))
            except:
                print("{} Still DOWN!".format(host))

hostlist = hostLoad()
print(hostCheck())
print(hostError())
#tup = Thread(target = hostCheck)
#tdown = Thread(target = hostError)
#tup.start()
#tdown.start()
