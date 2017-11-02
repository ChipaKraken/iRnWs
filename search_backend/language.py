# encoding=utf8
from re import findall as fa
from collections import defaultdict as dd

class LangChecker(object):
	"""docstring for LangChecker"""
	def __init__(self):
		self.langs = {}

	def training(self, lang, path):
		data = dd(int)
		with open(path) as book:
			book = book.read()
			for word in fa('\w+', book):
				temp = word.lower()
				data['^'+temp[:1]] += 1
				data[temp[-1:]+'$'] += 1
				while len(temp[:2]) == 2:
					data[temp[:2]] += 1
					data[temp[:1]] += 1
					temp = temp[1:]
		self.langs[lang] = dict(data)

	def check_word(self, word, lang):
		if (word[:2]) in self.langs[lang]:
			# print float(self.langs[lang][word[:2]])/sum(float(v) for k,v in self.langs[lang].items() if word[:1] in k[:1])
			return float(self.langs[lang][word[:2]])/sum(float(v) for k,v in self.langs[lang].items() if word[:1] in k[:1])
		else:
			first = float(self.langs[lang][word[:1]])/sum(float(v) for k,v in self.langs[lang].items() if len(k) == 1)
			secon = float(self.langs[lang][word[1]])/sum(float(v) for k,v in self.langs[lang].items() if len(k) == 1)
			return first*secon

	def check(self, sentence):
		result = dict.fromkeys(self.langs.keys(),1)
		for word in fa('\w+', sentence):
			temp = '^'+word.lower()+'$'
			while len(temp[:2]) == 2:
				for lang in self.langs.keys():
					result[lang] *= self.check_word(temp, lang)
				temp = temp[1:]
		return max(result, key=lambda k: result[k])

class AuthorChecker(object):
	"""docstring for LangChecker"""
	def __init__(self):
		self.langs = {}

	def training(self, lang, path):
		data = dd(int)
		with open(path) as book:
			book = book.read()
			for word in fa('\w+ \w+', book):
				temp = word.lower()
				word1, word2 = temp.split()
				print word1, word2
				data['^'+temp[:1]] += 1
				data[temp[-1:]+'$'] += 1
				while len(temp[:2]) == 2:
					data[temp[:2]] += 1
					data[temp[:1]] += 1
					temp = temp[1:]
		self.langs[lang] = dict(data)

	def check_word(self, word, lang):
		if (word[:2]) in self.langs[lang]:
			# print float(self.langs[lang][word[:2]])/sum(float(v) for k,v in self.langs[lang].items() if word[:1] in k[:1])
			return float(self.langs[lang][word[:2]])/sum(float(v) for k,v in self.langs[lang].items() if word[:1] in k[:1])
		else:
			first = float(self.langs[lang][word[:1]])/sum(float(v) for k,v in self.langs[lang].items() if len(k) == 1)
			secon = float(self.langs[lang][word[1]])/sum(float(v) for k,v in self.langs[lang].items() if len(k) == 1)
			return first*secon

	def check(self, sentence):
		result = dict.fromkeys(self.langs.keys(),1)
		for word in fa('\w+', sentence):
			temp = '^'+word.lower()+'$'
			while len(temp[:2]) == 2:
				for lang in self.langs.keys():
					result[lang] *= self.check_word(temp, lang)
				temp = temp[1:]
		return max(result, key=lambda k: result[k])

# checker = LangChecker()
checker = AuthorChecker()
checker.training('English', 'data/pg23488.txt')
checker.training('Dutch', 'data/pg18066.txt')
print checker.check('De ontdekker van Amerika')
print checker.check('The Discoverer of America')