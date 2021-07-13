from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twisted.internet import reactor
from twisted.internet import task



url = 'https://www.infobae.com/ultimas-noticias/'
soup = BeautifulSoup(requests.get(url).content,'html.parser')
content_news = soup.find_all('a','nd-feed-list-card')
link_news = list()
news = list()



##Extract information from content_news##
def extractInformation():
    for n in content_news:
        news.append(n.text)
        link_news.append('https://www.infobae.com/'+(n.get('href')))


def generateString():
    content = "Daily News"
    for i in range(0,11):
        content = content + '\n' + "\n" + news[i] +"\n"+"Link: " + link_news[i] + '\n'
    return content

##Prepare the email that will be send##
def sendEmail():
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        msg = MIMEMultipart()
        smtp.login('email_Login',"password")
        msg['From'] = 'email_from'
        msg['To'] = 'email_to'
        msg['Subject'] = 'News'
        message = generateString()
        msg.attach(MIMEText(message,'plain'))
        smtp.sendmail(msg['From'],msg['To'],msg.as_string())

def execute():
    extractInformation()
    sendEmail()
##Main##
Time = 3600.0 ##amount of seconds to the next execution##
RunTask = task.LoopingCall(execute)
RunTask.start(Time)
reactor.run()
