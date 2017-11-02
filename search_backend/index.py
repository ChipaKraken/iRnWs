import os, json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from collections import defaultdict

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
					yield {'name': file_path, 'doc': json.dumps(doc)}

class IndexFile(object):
	"""docstring for IndexFiles"""
	def __init__(self, file, id):
		self.tokenizer = RegexpTokenizer(r'\w+')
		self.stopwords = set(stopwords.words('english'))
		self.stemmer = EnglishStemmer()
		self.file = file
		self.id = id
	
	def get_data(self):
		index = defaultdict(defaultdict(list).copy)
		doc = self.file['doc']
		for start, end in self.tokenizer.span_tokenize(doc):
			token = doc[start:end].lower()
			if token in self.stopwords:
				continue
			index[self.stemmer.stem(token)][self.id].append(start)
		return index

books = FileReader("../python-3.6.3-docs-text/using")
book_count = 0
for x in books.read():
	tokens = IndexFile(x, book_count)
	book_count+=1
	print tokens.get_data()