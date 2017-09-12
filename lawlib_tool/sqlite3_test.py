import sqlite3

##part4 SELECT INFO
conn=sqlite3.connect('sqlite3_test.db')
print('opened database successfully')
c= conn.cursor()
cursor = c.execute("SELECT ID,NAME,ADDRESS,SALARY from COMPANY")
for row in cursor:
    print('ID=',row[0])
    print('NAME=', row[1])
    print('ADDRESS=', row[2])
    print('SALARY=', row[3],'\n')
print('Operation done successfully')
conn.close()




##part3 INSERT INFO
# conn=sqlite3.connect('sqlite3_test.db')
# print('opened database successfully')
# c= conn.cursor()
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) "
#           "VALUES(1,'PAUL',32,'CALIFORNIA',20000)");
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) "
#           "VALUES(2,'ALLEN',25,'TEXAS',15000)");
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) "
#           "VALUES(3,'TEDDY',23,'NORWAY',20000)");
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) "
#           "VALUES(4,'MARK',25,'RICH-MOND',65000)");
# conn.commit()
# print('records create successfully')
# conn.close()


##part2 create table
# conn=sqlite3.connect('sqlite3_test.db')
# print('opened database successfully')
# c= conn.cursor()
# c.execute('''CREATE TABLE COMPANY
# ( ID INT PRIMARY KEY NOT NULL,
# NAME  TEXT  NOT NULL,
# AGE INT NOT NULL,
# ADDRESS CHAR(50),
# SALARY REAL);''')
# print('table create successfully')
# conn.commit()
# conn.close()


##part1 connect database
# conn=sqlite3.connect('sqlite3_test.db')
# print('opened database successfully')


