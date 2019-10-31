import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

def send_mail(sender, sender_pwd, sender_name, receivers, host, subject, body, format):
    msg = MIMEText(body,format, _charset='utf-8')
    format_from = formataddr([sender_name,sender])
    msg['Subject'] = subject
    msg['From'] = format_from
    msg['To'] = ",".join(receivers) if type(receivers) is list else receivers
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    try:
        s = smtplib.SMTP()
        s.connect(host)
        s.ehlo()
        s.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'
        s.login(sender, sender_pwd)
        s.sendmail(sender, receivers, msg.as_string())
        s.close()
    except Exception as e:
        log.exception(e)
        return False
    return True

