import smtplib
from common import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

class mailSender:
    _from_addr = config.MAIL_FROM
    _to_addr = config.MAIL_TO

    @classmethod
    def sendMail(cls,_msg,_subject):
        msg = MIMEMultipart()
        msg['from'] = cls._from_addr
        msg['to'] = cls._to_addr
        msg['subject'] = _subject
        txt = MIMEText(_msg)
        msg.attach(txt)
        # try:
        server = smtplib.SMTP()
        server.connect(config.SMTP_HOST,config.SMTP_PORT)
        server.login(config.AUTH_USER,config.AUTH_PASSWD)
        server.sendmail(msg['from'],msg['to'],str(msg))
        server.quit()
        logger.info('主题为{}的邮件发送成功。'.format(_subject))
        # except Exception as e:
        #     logger.error('主题为{0}的邮件发送失败。错误信息:{1}'.format(_subject,e))


