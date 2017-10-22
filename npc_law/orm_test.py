from sqlalchemy import create_engine,Column,\
    String,Integer

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
engine=create_engine('mysql+mysqlconnector://root:alvincha@localhost:3306/test',echo=True)
#echo is true will show the process

##STEP1:create table
class User(Base):
    __tablename__='users'#tablename,not table,be careful
    id=Column(Integer,primary_key=True)
    name=Column(String(50))


Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()

#STEP5:QUERY
ret= session.query(User).filter_by(name='update name').all()
print(ret)
for i in ret:
    print(i.id,i.name)

ret1 = session.query(User).filter_by(name='update name').first()
print(type(ret1))
print(ret1.id,ret1.name)

# print name/mayun
ret2=session.query(User).filter(User.name.in_(['name','mayun'])).all()
print(ret2)
for i in ret2:
    print(i.id,i.name)

ret3=session.query(User.name.label('')).all()
print(ret3,type(ret3))

#print by order
ret4=session.query(User).order_by(User.name).all()
for i in ret4:
    print(i.id,i.name)

#limit area
ret5=session.query(User).order_by(User.id)[0:3]
for i in ret5:
    print(i.id,i.name)

#
user=session.query(User).filter(User.id=='5').one()
print(type(user),user.name)


#STEP4:UPDATE
# #update id>2's name
# session.query(User).filter(User.id>2).update({'name':'update name'})
# session.commit()


# #update id=2
# session.query(User).filter(User.id==2).update({'id':6})
# session.commit()


#add data
# session.add_all([
#     User(id=3,name='sbyao'),
#     User(id=4,name='liuyao'),
#     User(id=5,name='mayun'),
# ])
# session.commit()

#STEP3:DELETE DATA
# session.query(User).filter(User.id >2).delete()
# session.commit()



#STEP2:add data
# zengjia=User(id=2,name='sbliuyao')
# session.add(zengjia)
# session.add_all([
#         User(id=3,name='sbyao'),
#         User(id=4,name='liuyao')
#         ])
# session.commit()


# class Host(Base):
#     __tablename__='hosts'
#     id= Column(Integer,primary_key=True,autoincrement=True)
#     hostname=Column(String(64),unique=True,nullable=False)
#     ip_addr=Column(String(128),unique=True,nullable=False)
#     port=Column(Integer,default=22)
#
# Base.metadata.create_all(engine)
#
# if __name__=='__main__':
#     SessionCls=sessionmaker(bind=engine)
#     session=SessionCls()
#     h1=Host(hostname='qd115',ip_addr='115.29.51.8')
#     h2=Host(hostname='Ubuntu',ip_addr='139.129.5.191',port=80)
#     h3=Host(hostname='mysql',ip_addr='121.42.195.15',port=3306)
#     session.add_all([h1,h2,h3])
#     session.commit()



#
#
# Base= declarative_base()
# class User(Base):
#     __tablename__='user'
#     id=Column(String(20),primary_key=True)
#     name=Column(String(20))
#     #一对多
#     books=relationship('Book')
#
# class Book(Base):
#     __table__='book'
#     id=Column(String(20),primary_key=True)
#     name=Column(String(20))
#     user_id=Column(String(20),ForeignKey('user.id'))
#
# engine=create_engine('mysql+mysqlconnector://root:alvincha@localhost:3306/test')
# DBSession=sessionmaker(bind=engine)
# session=DBSession()
# user=session.query(User).filter(User.id=='5').one()
# print('type',type(user))
# print('name:',user.name)
# session.close()

#query
# class User(Base):
#     __tablename__='user'
#     id=Column(String(20),primary_key=True)
#     name=Column(String(20))
#
# engine=create_engine('mysql+mysqlconnector://root:alvincha@localhost:3306/test')
# DBSession=sessionmaker(bind=engine)
#
# session=DBSession()
# user=session.query(User).filter(User.id=='5').one()
# print('type',type(user))
# print('name:',user.name)
# session.close()




#add user
# class User(Base):
#     __tablename__='user'
#     id=Column(String(20),primary_key=True)
#     name=Column(String(20))
#
# engine=create_engine('mysql+mysqlconnector://root:alvincha@localhost:3306/test')
# DBSession=sessionmaker(bind=engine)
# session=DBSession()
# new_user=User(id='5',name='Bob')
# session.add(new_user)
# session.commit()
# session.close()