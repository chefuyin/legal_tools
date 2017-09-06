import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
'''
教程参见http://www.runoob.com/python3/python3-smtp.html
'''
mail_host ='smtp.qq.com'
mail_user ='chefuyin@foxmail.com'
mail_pass ='phbxkzjpgpckbjbf'

sender ='chefuyin@foxmail.com'
receivers =['289441327@qq.com','chefuyin0715@126.com']
date= formatdate(localtime=True)

message = MIMEMultipart()
message['From']= Header('法律速递<{}>'.format(sender),'utf-8')
message['To']=Header(" ; ".join(receivers),'utf-8')
subject ='Python SMTP email test'
message['Subject']=Header(subject,'utf-8')
message['Date']= date

#content
message.attach(MIMEText('THIS IS PYTHON EMAIL TEST','plain','utf-8'))
# filepath='工商总局关于调整工商登记前置审批事项目录的通知.txt'
filepath='1.txt'

part = MIMEBase('application','octet-stream')
part.set_payload(open(filepath,'rb').read())
encoders.encode_base64(part)
part.add_header(
    'Content-Disposition',
    'attachment; filename={}'.format(filepath)
)

message.attach(part)
# att1 = MIMEText(open(filepath,'rb').read(),'base64','utf-8')
# att1["Content-Type"]="application/octet-stream"
# att1["Contet-Disposition"]='attachment;filename={}'.format(filepath)
# print(att1)
# message.attach(att1)
try:
    smtpObj =smtplib.SMTP_SSL()
    smtpObj.connect(mail_host,465)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    print('success!')
except smtplib.SMTPException as e:
    print(e)
    print("error:can't send email!")


