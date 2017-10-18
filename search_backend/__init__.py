# encoding=utf8
import os
import nltk
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from collections import defaultdict
import json
import re

def read_all_files():
	data = []
	for root, dirs, files in os.walk('python-3.6.3-docs-text'):
		for file in files:
			file_path = os.path.join(root, file)
			with open(file_path) as auto:
				doc = auto.read()
				data.append({'name': file_path, 'doc': json.dumps(doc)})
	return data

def index_files():
	index = defaultdict(defaultdict(list).copy)
	for id, file in enumerate(files):
		doc = file['doc']
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
	search_results = defaultdict(int)
	temp_data = {}
	for word in re.findall('\w+', query_string):
		search_result = google.get(stemmer.stem(word))
		for x in search_result:
			search_results[x]+=1
			temp_data[x]=search_result[x][0]
	sorted(search_results.items(), key=lambda k_v: k_v[1], reverse=True)
	for x in search_results:
		result_list.append({
				'title': files[x]['name'],
				'snippet': files[x]['doc'][temp_data[x]-100:temp_data[x]+100],
				'href': 'https://docs.python.org/3'+files[x]['name'][22:-3]+'html'
			})
	return result_list
