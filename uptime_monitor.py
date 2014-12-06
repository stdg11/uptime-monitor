import os, sys, logging, configparser, requests, time, smtplib, datetime
from threading import Thread
#Configure Logging
logging.basicConfig(filename='output.log', level=logging.DEBUG)
logging.info('Started')
#Load config.ini
parser = configparser.ConfigParser() 
parser.read('config.ini')
# config.ini - enable of disable notifications
notifications = parser.get('NOTIFY','enabled')
## Add to config.ini
#Server to check
hostsfile = parser.get('GENERAL','hostsfile')
#Downtime hostlist
hostlist = {}
notified = ['']

# Check if users file exists, if not throw error
def hostLoad():
    if os.path.isfile(hostsfile):
        logging.info('Reading hosts from %s', hostsfile)
        with open(hostsfile, 'r') as hosts:
            for line in hosts:
                line = line.replace("\n","")
                servicehost = line.split(',')
                service = servicehost[0]
                host = servicehost[1]
                hostlist[host] = [service , False]
            logging.debug('Hosts: %s', hostlist)
    else:
        logging.error("Cannot find file specified, please try again.", exc_info=True)
        exit(0)

def notify(host, status, error):
    if notifications == True:
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
            print("Email sent to {}".format(mail_to))
            notified.append(host)
        except:
            smtp_error = ("{} exception {}".format(datetime.datetime.now(),sys.exc_info()[0]))
            logging.error(smtp_error)
            print("Error sending mail: {}".format(smtp_error))
    else:
        print('Notifications disabled')

def hostCheck():
    while True:
        print('Running Check...')
        for host,isdown in hostlist.items():
            try:
                check = requests.get(host)
                hostcode = check.status_code
                print(host,hostcode)
                if hostcode == requests.codes.ok:
                    logging.info("{} {} returned status code {}".format(datetime.datetime.now(),host,hostcode))
                    hostlist[host][1] = 0
                    #writeHTML(host, isdown)
                else:
                    error = ("{} ERROR! {} returned status code {}".format(datetime.datetime.now(),host,hostcode))
                    logging.error(error)
                    onError(host,error)
            except KeyboardInterrupt:
                break
            except:
                error = ("{} {} exception {}".format(datetime.datetime.now(),host,sys.exc_info()[0]))
                logging.error(error)
                print(error)
                onError(host,error)
        writeHTML(hostlist)
        time.sleep(60)

def onError(host,error):
    hostlist[host][1] = 1
    print(error)
    #start timer
    if host not in notified:
        notify(host, "DOWN!", error)
    else:
        print("Notification already sent")

#def hostError():
#    while True:
#        time.sleep(60)
#        for host,service,isdown in hostlist.items():
#            try:
#                check = requests.get(host)
#                hostcode = check.status_code
#                if hostcode == requests.codes.ok:
#                    error = ("{} {} Site back UP!".format(datetime.datetime.now(),host))
#                    logging.info(error)
#                    #hostlist[host] = False
#                    notify(host,"UP!",error)
#                else:
#                    print("{} Still DOWN!".format(host))
#            except:
#                print("{} Still DOWN!".format(host))

def writeHTML(hostlist):
    header = open("templates/header.html", "r")
    footer = open("templates/footer.html", "r")
    headerCont = header.read()
    footerCont = footer.read()
    text = headerCont
    for host in hostlist:
        if hostlist[host][1] == 0:
            upORdown = 'UP'
            colour = 'success'
        elif hostlist[host][1] == 1:
            upORdown = 'DOWN'
            colour = 'danger'
        text += '<tr class="{}"><td>{}</td><td>{}</td><td>{}</td></tr>'.format(colour, hostlist[host][0], host, upORdown)
    text += footerCont
    f = open("html/status.html","w")
    f.write(text)
    f.close()

hostLoad()
hostCheck()
