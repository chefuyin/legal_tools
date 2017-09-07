import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
import os
'''
教程参见http://www.runoob.com/python3/python3-smtp.html
'''
class SendEmail():
    def __init__(self):
        '''
        初始化设置发送邮箱、发件人、收件人等基本信息
        '''
        self.mail_host ='smtp.qq.com'
        self.mail_user ='chefuyin@foxmail.com'
        self.mail_pass ='phbxkzjpgpckbjbf'
        self.sender ='chefuyin@foxmail.com'
        self.receivers =['289441327@qq.com',]
        # self.receivers = ['289441327@qq.com','1172024261@qq.com','229107296@qq.com']
        self.time_tag= formatdate(localtime=True)
        self.date="-".join(self.time_tag.split(" ")[1:4])
        self.subject = '法律速递{}'.format(self.date)
        self.message = MIMEMultipart()#默认发送带附件的邮件，所以构建一个
        self.default_file_folder_path='E:\PycharmProjects\legal_tools\legal_tools\lawlib_tool\law'

    def main(self):
        '''构建邮件内容'''
        self.make_content()
        '''搜索文件夹，构建附件'''
        files = self.search_file_folder(self.default_file_folder_path)
        txt_files = self.get_attach_path(files)
        # print(txt_files)
        for file_path in txt_files:
            print(file_path)
            self.make_attach(file_path)
        '''发送邮件'''
        self.send_message()

    def make_content(self):
        self.message['From']= Header('法律速递<{}>'.format(self.sender),'utf-8')
        self.message['To']=Header(" ; ".join(self.receivers),'utf-8')
        self.message['Subject']=Header(self.subject,'utf-8')
        self.message['Date']= self.time_tag
        self.message.attach(MIMEText('Dear all,\n'+self.subject+'已发送，请注意查收，谢谢！！','plain','utf-8'))

    def search_file_folder(self,folder_path):
        if os.path.isdir(folder_path):
            file_list = os.listdir(folder_path)
            new_file_list=[]
            for file in file_list:
                new_file_path= folder_path+"\\"+file
                new_file_list.append(new_file_path)
            return new_file_list

        else:
            print('THIS IS NOT A FOLDER,PLEASE CHECK IT!')


    def get_attach_path(self,file_path_list):
        txt_path_list=[]
        for file_path in file_path_list:
            if file_path.split('.')[-1]=='txt':
                txt_path_list.append(file_path)
        return txt_path_list


    def make_attach(self,filepath):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(filepath, 'rb').read())
        filename = filepath.split('\\')[-1]
        # print(filename)
        encoders.encode_base64(part)

        '''调试前'''
        # new_filepath = filepath.replace('\\', '/')
        # print(new_filepath)
        # part = MIMEBase('application', 'octet-stream')
        # part.set_payload(open(new_filepath, 'rb').read())
        # filename = new_filepath.split('/')[-1]
        # # print(filename)
        # encoders.encode_base64(part)

        '''
        编码问题折磨死人，filename如果是中文要转为GBK，且不能用上面的表达式
        '''
        part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
        self.message.attach(part)

    def send_message(self):
        try:
            smtpObj =smtplib.SMTP_SSL()
            smtpObj.connect(self.mail_host,465)
            smtpObj.login(self.mail_user,self.mail_pass)
            smtpObj.sendmail(self.sender,self.receivers,self.message.as_string())
            print('success!')
        except smtplib.SMTPException as e:
            print(e)
            print("error:can't send email!")


if __name__ == '__main__':
    a = SendEmail()
    a.main()



# #content
# message.attach(MIMEText('THIS IS PYTHON EMAIL TEST','plain','utf-8'))
# # filepath='工商总局关于调整工商登记前置审批事项目录的通知.txt'
# filepath='1.txt'
#
# part = MIMEBase('application','octet-stream')
# part.set_payload(open(filepath,'rb').read())
# encoders.encode_base64(part)
# part.add_header(
#     'Content-Disposition',
#     'attachment; filename={}'.format(filepath)
# )
#
# message.attach(part)
# # att1 = MIMEText(open(filepath,'rb').read(),'base64','utf-8')
# # att1["Content-Type"]="application/octet-stream"
# # att1["Contet-Disposition"]='attachment;filename={}'.format(filepath)
# # print(att1)
# # message.attach(att1)
# try:
#     smtpObj =smtplib.SMTP_SSL()
#     smtpObj.connect(mail_host,465)
#     smtpObj.login(mail_user,mail_pass)
#     smtpObj.sendmail(sender,receivers,message.as_string())
#     print('success!')
# except smtplib.SMTPException as e:
#     print(e)
#     print("error:can't send email!")




