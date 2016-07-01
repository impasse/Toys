from sqlalchemy import create_engine,Column,String,Integer,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Option(Base):
    __tablename__ = 'typecho_options'
    name = Column(String,primary_key=True)
    user = Column(Integer,primary_key=True)
    value = Column(Text)

session = sessionmaker(bind=create_engine('mysql+pymysql://root:@localhost:3306/typecho'))()

for name,value in session.query(Option.name,Option.value).all():
    print("%s: %s"%(name,value))
