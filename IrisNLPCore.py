import sys
import nltk
import math
import time

import collections

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


def split_wordtags(brown_train):
    wordtags = []
    sentenceList = []
    brown_wordsInSentence = []
    brown_tagsInSentence = []
    brown_words = []
    brown_tags = []

    for line in brown_train:
        wordtagsInLine = line.split(' ')
        wordtagsInLine.insert(0, START_SYMBOL)
        wordtagsInLine.insert(0, START_SYMBOL)
        wordtagsInLine.remove('\r\n')
        wordtagsInLine.append(STOP_SYMBOL)
        sentenceList.append(wordtagsInLine)

    for sentence in sentenceList:
        for wordtag in sentence:
            if wordtag != START_SYMBOL and wordtag != STOP_SYMBOL:
                n = wordtag.rindex('/')
                word = wordtag[: n ]
                tag = wordtag[n + 1: ]
                brown_wordsInSentence.append(word)
                brown_tagsInSentence.append(tag)
            else:
                brown_wordsInSentence.append(wordtag)
                brown_tagsInSentence.append(wordtag)
        brown_words.append(brown_wordsInSentence)
        brown_tags.append(brown_tagsInSentence)
        brown_wordsInSentence = []
        brown_tagsInSentence = []

    return brown_words, brown_tags


def calc_trigrams(brown_tags):
    q_values = {}

    brown_tagsSeq = []
    for sentence in brown_tags:
        for tag in sentence:
            brown_tagsSeq.append(tag)
    brown_tags = brown_tagsSeq

    unigramsInBrownTags = brown_tags
    bigramsInBrownTags = list(nltk.bigrams(brown_tags))
    trigramsInBrownTags = list(nltk.trigrams(brown_tags))

    unigrams_c = collections.Counter(unigramsInBrownTags)
    bigrams_c = collections.Counter(bigramsInBrownTags)
    trigrams_c = collections.Counter(trigramsInBrownTags)

    unigram_p = {}
    bigram_p = {}

    unigrams_length = len(unigramsInBrownTags)
    bigrams_length = len(bigramsInBrownTags)
    trigram_length = len(trigramsInBrownTags)

    for i in range(unigrams_length - 1):
        if unigramsInBrownTags[i] == START_SYMBOL and unigramsInBrownTags[i+1] == START_SYMBOL:
            continue
        if unigramsInBrownTags[i] == STOP_SYMBOL:
            continue
        token = unigramsInBrownTags[i]
        unigram_p[token] = math.log(float(unigrams_c[token])/float(unigrams_length),2)

    for i in range(bigrams_length - 1):
        if bigramsInBrownTags[i][0] == STOP_SYMBOL:
            continue
        token = bigramsInBrownTags[i]
        bigram_p[token] = math.log(float(bigrams_c[token])/float(unigrams_c[token[0]]), 2)
        #bigram_p[token] = math.log(float(bigrams_c[token])/float(bigrams_length), 2) - unigram_p[token[0]]

    for i in range(trigram_length - 1):
        if trigramsInBrownTags[i][1] == STOP_SYMBOL or trigramsInBrownTags[i][0] == STOP_SYMBOL:
            continue
        token = trigramsInBrownTags[i]
        q_values[token] = math.log(float(trigrams_c[token]), 2) - bigram_p[(token[0], token[1])] - math.log(unigrams_c[token[0]],2)
        #q_values[token] = math.log(float(trigrams_c[token])/float(trigram_length), 2) - bigram_p[(token[0], token[1])] - unigram_p[token[0]]

    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()

def calc_known(brown_words):
    known_words = []

    brown_wordsSeq = []
    for sentence in brown_words:
        for word in sentence:
            brown_wordsSeq.append(word)
    brown_words = brown_wordsSeq

    wordFreCounter = collections.Counter(brown_words)

    for word in brown_words:
        n = wordFreCounter[word]
        if n <= 5:
            known_words.append((word,word))

    known_words = dict(known_words)

    return known_words

def replace_rare(brown_words, known_words):
    
    brown_words_rare = []

    brown_wordsSeq = []
    for sentence in brown_words:
        for word in sentence:
            brown_wordsSeq.append(word)
    brown_words = brown_wordsSeq

    brownWordsLength = len(brown_words)

    for i in range(brownWordsLength - 1):
        try:
            rareWord = known_words[brown_words[i]]
            brown_words_rare.append(RARE_SYMBOL)
        except:
            brown_words_rare.append(brown_words[i])

    return brown_words_rare


def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


def calc_emission(brown_words_rare, brown_tags):
    e_values = {}
    taglist = set([])
    wordWTagList = []

    brown_tagsSeq = []
    for sentence in brown_tags:
        for tag in sentence:
            brown_tagsSeq.append(tag)
    brown_tags = brown_tagsSeq

    wordListLength = len(brown_words_rare)

    for i in range(wordListLength - 1):
        wordWTagList.append((brown_words_rare[i],brown_tags[i]))
        e_values[(brown_words_rare[i],brown_tags[i])] = 0

    wordWTagListCounter = collections.Counter(wordWTagList)
    tagListCounter = collections.Counter(brown_tags)

    eValuesLength = len(e_values)
    eValuesKeyList = e_values.keys()

    for i in range(eValuesLength - 1):
        key = eValuesKeyList[i]
        e_values[key] = math.log(float(wordWTagListCounter[key])/float(wordListLength), 2) - math.log(float(tagListCounter[key[1]])/float(wordListLength), 2)

    taglist = tagListCounter.keys()


    return e_values, taglist

def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()

def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    tagged = []

    brownDevWordsLineCount = len(brown_dev_words)
    transitionProbList = {}
    stateProbList = {}
    scoreList = []

    for sentence in brown_dev_words:
        sentence.insert(0, START_SYMBOL)
        sentence.insert(0, START_SYMBOL)
        sentence.append(STOP_SYMBOL)
        originalSentence = sentence
        sentence = replace_rare([sentence], known_words)
        sentenceLength = len(sentence)
        maxStateValue = 0
        cumulativeMaxStateValue = 0
        chosenState_1 = ' '
        chosenState_2 = ' '

        #Initialization - First Time
        scoreList = []
        #print sentence[2]
        for tag in taglist:
            #print tag
            try:
                transitionProbList[(START_SYMBOL, START_SYMBOL, tag)] = q_values[(START_SYMBOL, START_SYMBOL, tag)]
                #print transitionProbList[(START_SYMBOL, START_SYMBOL, tag)]
            except:
                transitionProbList[(START_SYMBOL, START_SYMBOL, tag)] = -1000
                #print str(-1000)
            try:
                stateProbList[sentence[2],tag] = e_values[sentence[2],tag]
                #print stateProbList[sentence[2],tag]
            except:
                stateProbList[sentence[2],tag] = -1000
                #print str(-1000)
            scoreList.append(0 + transitionProbList[(START_SYMBOL, START_SYMBOL, tag)] + stateProbList[sentence[2],tag])

        maxStateValue = max(scoreList)
        cumulativeMaxStateValue = cumulativeMaxStateValue + maxStateValue
        chosenState_1 = taglist[scoreList.index(maxStateValue)]
        tagged.append(str(originalSentence[2]) + '/' + str(chosenState_1) + ' ')

        #Initialization - Second Time
        scoreList = []
        #print sentence[3]
        for tag in taglist:
            #print tag
            try:
                transitionProbList[(START_SYMBOL, chosenState_1, tag)] = q_values[(START_SYMBOL, chosenState_1, tag)]
                #print transitionProbList[(START_SYMBOL, chosenState_1, tag)]
            except:
                transitionProbList[(START_SYMBOL, chosenState_1, tag)] = -1000
                #print str(-1000)
            try:
                stateProbList[sentence[3],tag] = e_values[sentence[3],tag]
                #print stateProbList[sentence[3],tag]
            except:
                stateProbList[sentence[3],tag] = -1000
                #print str(-1000)
            scoreList.append(cumulativeMaxStateValue + transitionProbList[(START_SYMBOL, chosenState_1, tag)] + stateProbList[sentence[3],tag])

        maxStateValue = max(scoreList)
        cumulativeMaxStateValue = cumulativeMaxStateValue + maxStateValue
        chosenState_2 = taglist[scoreList.index(maxStateValue)]
        tagged.append(str(originalSentence[3]) + '/' + str(chosenState_2) + ' ')

        #Let's Do This!
        for i in range(sentenceLength - 5):
            scoreList = []
            #print sentence[i+4]
            for tag in taglist:
                #print tag
                try:
                    transitionProbList[(chosenState_1, chosenState_2, tag)] = q_values[(chosenState_1, chosenState_2, tag)]
                    #print transitionProbList[(chosenState_1, chosenState_2, tag)]
                except:
                    transitionProbList[(chosenState_1, chosenState_2, tag)] = -1000
                    #print str(-1000)
                try:
                    stateProbList[sentence[i+4],tag] = e_values[sentence[i+4],tag]
                    #print stateProbList[sentence[i+4],tag]
                except:
                    stateProbList[sentence[i+4],tag] = -1000
                    #print str(-1000)
                scoreList.append(cumulativeMaxStateValue + transitionProbList[(chosenState_1, chosenState_2, tag)] + stateProbList[sentence[i+4],tag])

            maxStateValue = max(scoreList)
            cumulativeMaxStateValue = cumulativeMaxStateValue + maxStateValue
            chosenState_1 = chosenState_2
            chosenState_2 = taglist[scoreList.index(maxStateValue)]
            tagged.append(str(originalSentence[i+4]) + '/' + str(chosenState_2) + ' ')

        tagged.append('\r\n')

    return tagged

def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    for sentence in brown_words:
        for word in sentence:
            if word == START_SYMBOL:
                sentence.remove(START_SYMBOL)
            if word == STOP_SYMBOL:
                sentence.remove(STOP_SYMBOL)

    for sentence in brown_tags:
        for word in sentence:
            if word == START_SYMBOL:
                sentence.remove(START_SYMBOL)
            if word == STOP_SYMBOL:
                sentence.remove(STOP_SYMBOL)

    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]
    #print training

    tagged = []

    nltkDefaultTagger = nltk.tag.sequential.DefaultTagger('NOUN')
    nltkBigramTagger = nltk.tag.sequential.NgramTagger(n = 2, train = training, backoff = nltkDefaultTagger)
    nltkTrigramTagger = nltk.tag.sequential.NgramTagger(n = 3, train = training, backoff = nltkBigramTagger)
    sentenceList = []
    sentenceInList = []
    for i in range(len(brown_dev_words)):
        sentenceInList = []
        for word, tag in nltkTrigramTagger.tag(brown_dev_words[i]):
            if word != START_SYMBOL and word != STOP_SYMBOL:
                entry = str(word) + '/' + str(tag) + ' '
                sentenceInList.append(entry)
            if word == STOP_SYMBOL:
                entry = '\r\n'
                sentenceInList.append(entry)
        sentenceList.append(sentenceInList)

    tagged = sentenceList
    #print tagged[0]
    return tagged


def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        #print sentence
        outfile.writelines(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols 
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities 
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' 
    brown_words_rare = replace_rare(brown_words, known_words)

    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities 
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    del brown_train
    del brown_words_rare

    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)


    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')


    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)


    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')


if __name__ == "__main__": main()
