from IrisNLPCore import *
def IrisNLPTopicExtractor_Train():
	#Loading Training Data
	infile = open("data/Brown_tagged_train.txt", "r")
	brown_train = infile.readlines()
	infile.close()

	#Split Words and Tags From Training Data
	brown_words, brown_tags = split_wordtags(brown_train)

	#Calculate Param q_values
	q_values = calc_trigrams(brown_tags)

	known_words = calc_known(brown_words)
	brown_words_rare = replace_rare(brown_words, known_words)

	#Calculate Param e_values / Generate taglists
	e_values, taglist = calc_emission(brown_words_rare, brown_tags)

	return taglist, known_words, q_values, e_values

def IrisNLPTopicExtractor(data_to_tag, result_path, taglist, known_words, q_values, e_values):

	data_to_tag_words = []
	for sentence in data_to_tag:
		data_to_tag_words.append(sentence.split(" ")[:-1])

	data_to_tag_words_noemptycells = []
	for i in data_to_tag_words:
		if i != [] and len(i) >= 2:
			data_to_tag_words_noemptycells.append(i)

	#print data_to_tag_words_noemptycells

	viterbi_tagged = viterbi(data_to_tag_words_noemptycells, taglist, known_words, q_values, e_values)

	#print viterbi_tagged

	q5_output(viterbi_tagged, result_path)