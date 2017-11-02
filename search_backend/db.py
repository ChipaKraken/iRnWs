from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

engine = create_engine('postgresql://python:jylan@localhost/kraken')
metadata = MetaData()
Base = declarative_base()
Base.metadata.bind = engine

class Docs(Base):
	__tablename__ = 'docs'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, unique=True)

class Words(Base):
	__tablename__ = 'words'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, unique=True)

class Index(Base):
	__tablename__ = 'index'
	id = Column(Integer, primary_key=True, autoincrement=True)
	doc_id = Column(Integer, ForeignKey(Docs.id))
	word_id = Column(Integer, ForeignKey(Words.id))
	beg = Column(Integer)

def doc_exists(name):
	return session.query(exists().where(Docs.name==name)).scalar()

def word_exists(name):
	return session.query(exists().where(Words.name==name)).scalar()


Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()