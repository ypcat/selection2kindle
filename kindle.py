#!/usr/bin/python

"""
Dependency: web.py, mod_wsgi for apache(optional)

Add to /etc/apache2/httpd.conf:

    WSGIScriptAlias /kindle /home/kindle/cgi-bin/kindle.py
    AddType text/html .py
    <Directory "/home/kindle/cgi-bin">
        Order deny,allow
        Allow from all
    </Directory>
    LimitRequestLine 32768
"""

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
        if i.body.strip() == '':
            return 'Select text to be sent to kindle and click the bookmarklet!'
        if 'title' not in i:
            i.title, i.body = i.body.split('\n', 1)
        send2kindle(**i)
        return '<pre>Done! You can close this window now.\nSent to: %s\nTitle: %s\nBody: %s</pre>' % (i.to, i.title, i.body)

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
application = app.wsgifunc() # or standalone without mod_wsgi: app.run()

