from decimal import MIN_EMIN
import smtplib
import random
from email.mime.text import MIMEText
from email.header import Header

smtp_server = 'smtp.sendgrid.net'
# 輸入smtp伺服器位置
port = 587
# 輸入使用smtp服務的連接埠

smtp_account = 'account'
#輸入帳號
smtp_password = 'api_key'
#輸入密碼

server = smtplib.SMTP(smtp_server, 587)

server_res = server.ehlo()
# print(f'res 1==> {server_res}')
# #測試smtp服務是否可以使用若能使用會回傳250

smtp_ttls = server.starttls()
# print(f'start tls ==> {smtp_ttls}')
# #測試tls服務是否可以使用若能使用會回傳220

smtp_login = server.login(smtp_account, smtp_password)
print(f'SMTP login ==> {smtp_login}')

message = MIMEText('您的驗證碼是:'+str(random.randrange(100000,999999)),'plain','utf-8')
message['From'] = Header('identity', 'utf-8')
message['To']=Header('Test','utf-8')

subject = 'IoT App 登入驗證碼'

message['Subject']=Header(subject,'utf-8')

server.sendmail('iotkuapp@gmail.com', "zwei3125@gmail.com",
                message.as_string())
# mail_options=(),
# rcpt_options=())


server.quit()