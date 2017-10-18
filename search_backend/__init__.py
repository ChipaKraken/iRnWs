# encoding=utf8
import os
import nltk
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from collections import defaultdict

def read_all_files():
	data = []
	for root, dirs, files in os.walk('python-3.6.3-docs-text'):
		for file in files:
			file_path = os.path.join(root, file)
			with open(file_path) as auto:
				doc = auto.read()
				data.append({'name': file_path, 'doc': doc})
	return data

def index_files():
	index = defaultdict(defaultdict(list).copy)
	for id, file in enumerate(files):
		doc = file['doc'].decode('utf-8')
		for start, end in tokenizer.span_tokenize(doc):
			token = doc[start:end].lower()
			if token in stopwords:
				continue
			index[stemmer.stem(token)][id].append(start)
	return index

tokenizer = RegexpTokenizer(r'\w+')
stopwords = set(stopwords.words('english'))
stemmer = EnglishStemmer()
files = read_all_files()
google = index_files()


def search(query_string):
	result_list = []
	search_result = google.get(query_string)
	for x in search_result:
		result_list.append({
			'title': files[x]['name'],
			'snippet': files[x]['doc'][search_result[x][0]-100:search_result[x][0]+100],
			'href': 'https://docs.python.org/3'+files[x]['name'][22:-3]+'html'
		})
	return result_list
