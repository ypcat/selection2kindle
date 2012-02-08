#!/usr/bin/python

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
import web

From = 'kindle@eumacro.csie.org'

class index:
    def GET(self):
        i = web.input()
        if i.to == 'YOURNAME@free.kindle.com':
            return 'Change %s in bookmarklet to your address' % i.to
        i.body = reformat(i.body)
        send2kindle(**i)
        return '<pre>%s sent to %s\n\n%s</pre>' % (i.title, i.to, i.body)

def reformat(s):
    s = re.sub('</tr>', '\n', s)
    s = re.sub('<[^>]+>', '', s)
    s = re.sub('&nbsp;', '', s)
    return s

def send2kindle(title, body, to):
    msg = MIMEMultipart()
    msg['From'] = From
    msg['To'] = to
    att = MIMEText(body.encode('utf-8'), 'plain', 'utf8')
    att.add_header('Content-Disposition', 'attachment', filename=title+'.txt')
    msg.attach(att)
    s = smtplib.SMTP('localhost')
    s.sendmail(From, [to], msg.as_string())
    s.quit()

app = web.application(('/','index'), globals())
application = app.wsgifunc()

