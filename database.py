from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine("sqlite:///todooo.db")


Base=declarative_base()


class ToDo(Base):
    __tablename__='todos'
    id=Column(Integer,primary_key=True)
    task=Column(String(256))


