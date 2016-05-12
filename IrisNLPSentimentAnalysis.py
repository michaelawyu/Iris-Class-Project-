def IrisNLPSentimentAnalysis_Load():
	f = open('data/AFINN-111.txt', 'r')
	AFINN_rawdata = f.readlines()
	f.close()
	AFINN = {}
	splitted_entry = []
	for entry in AFINN_rawdata:
		splitted_entry = entry[:-1].split('\t')
		AFINN[splitted_entry[0]] = splitted_entry[1]
	return AFINN

def IrisNLPSentimentAnalysis(sentence_collection, AFINN):
	score = 0
	words = []
	for sentence in sentence_collection:
		splitted_sentence = sentence.split(' ')
		a = 1	
		for word in splitted_sentence:
			print word
			words.append(word)
			try:
				#print score
				if word in ["not", "can't","never","no","wouldn't","haven't","cannot","doesn't","don't","hasn't","isn't","aren't","couldn't","shouldn't","didn't","weren't","shalln't"]:
					a = -1
				if int(AFINN[word.lower()]) > 0:
					score = score + a * int(AFINN[word.lower()])
				else:
					score = score + a * int(AFINN[word.lower()])
				print a * int(AFINN[word.lower()])
			except:
				score = score

	try:			
		weighted_score = float(score)/float(len(words))
		weighted_score = weighted_score * 20
	except:
		weighted_score = 0

	return weighted_score

