from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twisted.internet import reactor
from twisted.internet import task



url = 'https://www.infobae.com/ultimas-noticias/'
soup = BeautifulSoup(requests.get(url).content,'html.parser')
content_notice = soup.find_all('a','nd-feed-list-card')
link_notice = list()
notice = list()



##Extract information from content_notice##
def extractInformation():
    for n in content_notice:
        notice.append(n.text)
        link_notice.append('https://www.infobae.com/'+(n.get('href')))


def generateString():
    content = ""
    for i in range(0,11):
        content = content + '\n' + "Noticia " + str(i) + "\n" + notice[i] +"\n"+"Link: " + link_notice[i] + '\n'
    return content

##Prepare the email that will be send##
def sendEmail():
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        msg = MIMEMultipart()
        smtp.login('nellyesthercordiviola@gmail.com',"bolivar2760")
        msg['From'] = 'nellyesthercordiviola@gmail.com'
        msg['To'] = 'penenorysantiago@gmail.com'
        msg['Subject'] = 'Noticias'
        message = generateString()
        msg.attach(MIMEText(message,'plain'))
        smtp.sendmail(msg['From'],msg['To'],msg.as_string())

def execute():
    extractInformation()
    sendEmail()
##Main##



RunTask = task.LoopingCall(execute)
RunTask.start(3600.0)
reactor.run()
