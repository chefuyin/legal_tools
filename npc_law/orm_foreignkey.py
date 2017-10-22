from sqlalchemy import create_engine,func,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,Sequence
from sqlalchemy.orm import sessionmaker,relationship,backref

Base=declarative_base()
engine= create_engine("mysql+mysqlconnector://root:alvincha@localhost:3306/test",echo=True)

#3.多对多之三表外键关联
Host2Group=Table('host_2_group',Base.metadata,
                 Column('host_id',ForeignKey('host.id'),primary_key=True),
                 Column('group_id',ForeignKey('group.id'),primary_key=True),)
class Host(Base):
    __tablename__='hosts'
    id=Column(Integer,primary_key=True,autoincrement=True)
    hostname=Column(String(64),unique=True,nullable=False)
    ip_addr=Column(String(128),unique=True,nullable=False)
    port=Column(Integer,default=22)
    groups=relationship('Group',secondary=Host2Group,
                        backref='host_list')

class Group(Base):
    __tablename__='group'
    id=Column(Integer,primary_key=True)
    name=Column(String(64),unique=True,nullable=False)

if __name__=='__main__':
    SessionCls=sessionmaker(bind=engine)
    session=SessionCls()
    g1=Group(name='g1')
    g2 = Group(name='g2')
    g3 = Group(name='g3')
    g4 = Group(name='g4')
    session.add_all([g1,g2,g3,g4])
    session.commit()

# 2.多对多
# class Parent(Base):
#     __tablename__='parent'
#     id= Column(Integer,primary_key=True)
#     name=Column(String(64),unique=True,nullable=False)
#     children=relationship("Child",back_populates="parent")
#
# class Child(Base):
#     __tablename__='child'
#     id=Column(Integer,primary_key=True)
#     name=Column(String(64),unique=True,nullable=False)
#     parent_id=Column(Integer,ForeignKey('parent.id'))
#     parent=relationship("Parent",back_populates="children")
# Base.metadata.create_all(engine)
# if __name__=='__main__':
#     SessionCls=sessionmaker(bind=engine)
#     session=SessionCls()
#     mama=Parent(id='1',name='mamaxx')
#     baba=Parent(id='2',name='babaoo')
#     session.add_all([mama,baba])
#     onesb=Child(id='1',name='onesb',parent_id='2')
#     twosb=Child(id='2',name='twosb',parent_id='2')
#     session.add_all([onesb,twosb])
#     session.commit()

#1.一对多
# class User(Base):
#     __tablename__='user'
#     id=Column(String(20),primary_key=True)
#     name=Column(String(20))
#     books=relationship('Book')
# class Book(Base):
#     __tablename__='book'
#     id=Column(String(20),primary_key=True)
#     name=Column(String(20))
#     user_id=Column(String(20),ForeignKey('user.id'))
#
# Base.metadata.create_all(engine)
#
# if __name__=='__main__':
#     SessionCls=sessionmaker(bind=engine)
#     session=SessionCls()
#     liuyao= User(id='1',name='liuyao')
#     ali=User(id='2',name='ali')
#     session.add_all([liuyao,ali])
#     session.commit()
#     Whitedeer= Book(id='1',name='White_deer',user_id='1')
#     Threebody=Book(id='2',name='Three_body',user_id='2')
#     session.add_all([Whitedeer,Threebody])
#     session.commit()