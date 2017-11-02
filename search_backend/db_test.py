with engine.connect() as conn:
	docs = Docs(name='korn1235')
	if doc_exists(docs.name):
		docs = session.query(Docs).filter_by(name=docs.name).first()
	else:
		session.add(docs)
		session.commit()
	print docs.id

	words = Words(name='kraken15')
	if word_exists(words.name):
		words = session.query(Words).filter_by(name=words.name).first()
	else:
		session.add(words)
		session.commit()
	print words.id

	index = Index(doc_id=docs.id, word_id=words.id, beg=519)
	session.add(index)
	session.commit()
	print index.id