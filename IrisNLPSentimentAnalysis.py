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
		words.extend(sentence.split(' '))		
	for word in words:
		try:
			score = score + AFINN[word.lower()]
		except:
			score = score
	return (score/len(words)*20)

