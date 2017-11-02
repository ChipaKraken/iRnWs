from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
# from sqlalchemy.dialects.postgresql import insert
engine = create_engine('postgresql://python:jylan@localhost/kraken')
metadata = MetaData()

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
	__tablename__ = 'person'
	id = Column(Integer, primary_key=True)
	name = Column(String)

words = Table('words',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('word', String)
)
with engine.connect() as conn:
	ins = words.select()
	# ins = words.insert().values(word=['number','kraken', 'eshkere']).returning(Column('id'))
	result = conn.execute(ins)
	# # print dir(result)
	# # conn.execute(a)
	# # a = conn.execute("INSERT INTO public.words(word)VALUES ('number');")
	for x in result:
		print x