import os, json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from collections import defaultdict
from bz2 import BZ2File as bzopen
import xml.etree.ElementTree as ET
from tqdm import tqdm

from db import *

class FileReader(object):
	"""docstring for FileReader"""
	def __init__(self, path):
		self.path = path
	def read(self):
		for root, dirs, files in os.walk(self.path):
			for file in files:
				file_path = os.path.join(root, file)
				with open(file_path) as auto:
					doc = auto.read()
					docs = Docs(name=file_path)
					if doc_exists(docs.name):
						docs = session.query(Docs).filter_by(name=docs.name).first()
					else:
						session.add(docs)
						session.commit()
					yield {'id': docs.id, 'doc': json.dumps(doc)}

class IndexFile(object):
	"""docstring for IndexFiles"""
	def __init__(self, id, doc):
		self.tokenizer = RegexpTokenizer(r'\w+')
		self.stopwords = set(stopwords.words('english'))
		self.stemmer = EnglishStemmer()
		self.doc = doc
		self.id = id
	
	def get_data(self):
		for start, end in self.tokenizer.span_tokenize(self.doc):
			token = self.doc[start:end].lower()
			if token in self.stopwords:
				continue
			words = Words(name=token)
			if word_exists(words.name):
				words = session.query(Words).filter_by(name=words.name).first()
			else:
				session.add(words)
				session.commit()
			index = Index(doc_id=self.id, word_id=words.id, beg=start)
			session.add(index)
		session.commit()

class WikiReader(object):
	"""docstring for ClassName"""
	def __init__(self, path):
		self.file = bzopen(path)
		
	def readNextPage(self):
		page = ''
		for line in self.file:
			line = str(line).strip()
			if line == '<page>':
				page = line
			elif line == '</page>':
				page += '\n' + line
				yield ET.fromstring(page)
			elif page != '':
				page += '\n' + line

wiki = WikiReader('../../../enwiki-20171020-pages-articles1.xml-p10p30302.bz2')
for p in tqdm(wiki.readNextPage()):
	title = p.find('title').text
# for p in tqdm(wiki.readNextPage()):
# 	title = p.find('title').text
# 	try:
# 		title = p.find('redirect').attrib['title']
# 	except Exception as e:
# 		pass
# 	id = Docs(name=title)
# 	if doc_exists(id.name):
# 		id = session.query(Docs).filter_by(name=id.name).first()
# 	else:
# 		session.add(id)
# 		session.commit()
# 	doc = p.find('revision').find('text').text
# 	tokens = IndexFile(id.id, doc)
# 	tokens.get_data()


# books = FileReader("data/")
# for x in books.read():
# 	tokens = IndexFile(x['id'], x['doc'])