import smtplib
import random
from email.mime.text import MIMEText
from email.header import Header
import datetime

ADMIN = 'cavedairy@newlifedef.com'
def generate_safe_code():
    code = ''
    for i in range(6):
        code += str(random.randint(0,9))
    return code

def send_code_to_email(dst, src = ADMIN):
    code = generate_safe_code()
    try:
        message = MIMEText('Your code is ' + code + '\nEnter it in the website to finish register', 'plain', 'utf-8')
        message['From'] = Header("CaveDiary", 'utf-8')
        message['To'] = Header("收件人", 'utf-8')
        message['Subject'] = Header('Verify code', 'utf-8')
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        server.login(src, 'Hr3FSDAMZxuo7bj2')
        server.sendmail(src, dst, message.as_string())
    except:
        return -1
    return code

class Register_code:
    code_in_list = {}
    # TODO: Add time and update to block frequent request. DATA format: {username:[code,time]}, update every call
    # Using
    def add(self,username,code):
        current_time = datetime.datetime.now()
        self.code_in_list[username] = [code, current_time]


    def check(self,username,code):
        current_time = datetime.datetime.now()
        if username in self.code_in_list:
            if (current_time - self.code_in_list[username][1]).seconds > 600:
                return -1
            if self.code_in_list[username][0] == code:
                return 1
        return 0
register_code = Register_code()