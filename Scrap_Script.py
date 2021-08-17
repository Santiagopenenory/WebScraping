from email import message, message_from_binary_file
from warnings import resetwarnings
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
        link_news.append("https://www.infobae.com/"+(n.get('href')))


#####Generate HTML content
def generatePyH(title,link,picture):
    h='<h3 style="font: size 24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">'+title+'</h3>' 
    p = '<p>  </p>'
    i = '<img src='+picture+' width="400" height="200">'
    a= '<form action='+link+'><input type="submit" value="Seguir Leyendo"/></form>'
    return h+'\n'+i+'\n'+'\n'+p+'\n'+a+'\n'+p

def generateHTML(news,link_news):
    html = ""
    for i in range(0,9):
        html = html +'\n' + generatePyH(news[i],link_news[i])
    return html


def sendEmail():
    message = """

            <!DOCTYPE html>
    <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <title></title>
    <!--[if mso]>
    <noscript>
        <xml>
        <o:OfficeDocumentSettings>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    <style>
        table, td, div, h1, p {font-family: Arial, sans-serif;}
    </style>
    </head>
    <body style="margin:0;padding:0;">
    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
        <tr>
        <td align="center" style="padding:0;">
            <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
            <tr>
                <td align="center" style="padding:40px 0 30px 0;background:#FFFFFF;">
                <img src="https://www.ubp.edu.ar/wp-content/uploads/2016/12/INFOBAE-LOGO.png" alt="" width="250" style="height:auto;display:block;" />
                </td>
            </tr>
            <tr>
                <td style="padding:36px 30px 42px 30px;">
                <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                    <tr>
                    <td style="padding:0 0 36px 0;color:#153643;">
                    <h1>Daily News</h1>
                """
    message_e = """
                </td>
                    </tr>
                <tr>
                <td style="padding:30px;background:#F68E1E;">
                <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                    <tr>
                    <td style="padding:0;width:50%;" align="left">
                        <p style="margin:0;font-size:14px;line-height:16px;font-family:Arial,sans-serif;color:#ffffff;">
                        &reg; Infobae, "Hacemos Periodismo"<br/><a href="http://www.example.com" style="color:#ffffff;text-decoration:underline;"></a>
                        </p>
                    </td>
                    <td style="padding:0;width:50%;" align="right">
                        <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                        <tr>
                            <td style="padding:0 0 0 10px;width:38px;">
                            <a href="http://www.twitter.com/infobae" style="color:#ffffff;"><img src="https://assets.codepen.io/210284/tw_1.png" alt="Twitter" width="38" style="height:auto;display:block;border:0;" /></a>
                            </td>
                            <td style="padding:0 0 0 10px;width:38px;">
                            <a href="http://www.facebook.com/infobae" style="color:#ffffff;"><img src="https://assets.codepen.io/210284/fb_1.png" alt="Facebook" width="38" style="height:auto;display:block;border:0;" /></a>
                            </td>
                        </tr>
                        </table>
                    </td>
                    </tr>
                </table>
                </td>
            </tr>
            </table>
        </td>
        </tr>
    </table>
    </body>
    </html>
        
                """
    message = message +'\n'+generateHTML(news,link_news)+'\n' + message_e
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        msg = MIMEMultipart()
        smtp.login('email_User',"Password")
        msg['From'] = 'email_User'
        msg['To'] = 'recipient_mail'
        msg['Subject'] = 'News'
        msg['Content-type'] = 'text/html'
        msg.attach(MIMEText(message,'html'))
        smtp.sendmail(msg['From'],msg['To'],msg.as_string())

def execute():
    extractInformation()
    sendEmail()




RunTask = task.LoopingCall(execute)
RunTask.start(10.0) #Execution after 10 seconds#
reactor.run()
