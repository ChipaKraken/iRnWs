# encoding=utf8
import os
import nltk
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from collections import defaultdict
from db import *
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


def search_file(query_string):
	result_list = []
	search_results = defaultdict(int)
	temp_data = {}
	for word in re.findall('\w+', query_string):
		if word in stopwords:
			continue
		search_result = google.get(stemmer.stem(word))
		if search_result == None:
			continue
		for x in search_result:
			search_results[x]+=len(search_result[x])
			temp_data[x]=search_result[x][0]
	search_results = sorted(search_results.items(), key=lambda k_v: k_v[1], reverse=True)
	for x,y in search_results:
		result_list.append({
				'title': files[x]['name'],
				'snippet': files[x]['doc'][temp_data[x]-100:temp_data[x]+100],
				'href': 'https://docs.python.org/3'+files[x]['name'][22:-3]+'html'
			})
	return result_list


def search(query_string):
	result_list = []
	search_results = defaultdict(int)
	res = defaultdict(float)
	word_ids = []
	for word in re.findall('\w+', query_string):
		if word in stopwords:
			continue
		words = session.query(Words).filter_by(name=stemmer.stem(word.lower())).first()
		word_ids.append(words.id)
	results = session.query(
		Index.doc_id
	).filter(
		Docs.id == Index.doc_id,
		Index.word_id.in_(word_ids)
	).distinct(
		Docs.name
	).all()
	newlist = []
	for i, in results:
		if i not in newlist:
			newlist.append(i)
	frq = session.query(
		Index.doc_id,
		func.count(Index.doc_id)
	).group_by(Index.doc_id).filter(
		Index.doc_id.in_(newlist),
		Index.word_id.in_(word_ids)
	).all()
	amt = session.query(
		Index.doc_id,
		func.count(Index.doc_id)
	).group_by(Index.doc_id).filter(
		Index.doc_id.in_(newlist)
	).all()
	for i, c in frq:
		res[i] = c
	for i, c in amt:
		res[i] /= float(c)
	search_results = dict(res)
	search_results = dict(sorted(search_results.items(), key=lambda k_v: k_v[1], reverse=True))
	
	results = session.query(
		Docs.id,
		Docs.name
	).filter(
		Docs.id.in_([x-1 for x in search_results.keys()])
	).all()
	for id, doc_name in results:
		result_list.append({
				'title': doc_name,
				'snippet': search_results[id+1],
				'href': 'https://en.wikipedia.org/wiki/'+'_'.join(doc_name.split(' '))
			})
	return result_list
	# return results

print search('leo davinci')
# 	print word.name
# 	print index.beg
# 	print '-------------------------------'
