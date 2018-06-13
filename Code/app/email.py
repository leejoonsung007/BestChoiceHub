from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

# 这里可以去改一下邮件的内容，改成适合我们的邮件 在templates/auth/email/confirm.txt
# 其它的html文件也作出相应的更改 比如换个名字啊
# 这些html文件比如index.html 都是用了jinja模版，去熟悉一下jinja模版
