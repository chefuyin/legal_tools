import json,os,time


path='E:\PycharmProjects\legal_tools\legal_tools\lawlib_tool\law'
files= os.listdir(path)
dict1=''
dictMerged=dict(dict1)
all1=''
for file in files:
    data= {
        'title':file.split('.')[0],
        'status':'exsist',
        'time_tag':time.time(),
        'email_status':''
    }

import sqlite3

# conn =sqlite3.connect('law.db')
# cursor =conn.cursor()
# cursor.execute('create table user(id varchar(20)primary key,name varchar(20))')
# cursor.execute('insert into user(id,name) values(\'1\', \'Michael\')')
# print(cursor.rowcount)
# cursor.close()
# conn.commit()
# conn.close()

conn =sqlite3.connect('law.db')
cursor=conn.cursor()
cursor.execute('select * from user where id=?',('1',))
values=cursor.fetchall()
print(values)
cursor.close()
conn.close()


