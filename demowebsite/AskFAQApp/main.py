import numpy as np
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet
from collections import defaultdict
from itertools import islice
import operator

FAQ_DATA_SET = 'AskFAQApp/data/dataset.txt'


class Lemmatizer():
	
	lmtzr = WordNetLemmatizer()

	@staticmethod
	def getWordnetPos(tag):
	 if tag.startswith('J'):
		 return wordnet.ADJ
	 elif tag.startswith('V'):
		 return wordnet.VERB
	 elif tag.startswith('N'):
		 return wordnet.NOUN
	 elif tag.startswith('R'):
		 return wordnet.ADV
	 else:
		 return wordnet.NOUN

	@staticmethod
	def performLemmatization(data):
		wordArray = word_tokenize(data)
		tagged = nltk.pos_tag(wordArray)
		for index,word in enumerate(wordArray):
			if(len(word)>3):
				wordArray[index] = Lemmatizer.lmtzr.lemmatize(word,Lemmatizer.getWordnetPos(tagged[index][1]))                
		return ' '.join(word for word in wordArray)


class DataTrainer(object):

	def __init__(self,location,seperator):
		self.dataLocation = location
		self.seperator =seperator
		self.df = None
		self.cv = None
		self.rankMatrix = None
		self.vocabulary = None
		self.threshold = 0.40


	def LoadDataSet(self):
		self.df = pd.read_csv(self.dataLocation,sep=self.seperator)
		print("Total Questions Loaded:: "+ str(len(self.df)))


	def applyLemma(self):
		for index,question in enumerate(self.df['Question']):
			x = Lemmatizer.performLemmatization(question)
			self.df.loc[index,'TrimQuestion']=x
			#print(self.df['Question'][index])

	def applyCV(self):
		self.cv = TfidfVectorizer(min_df=1,stop_words='english')
		x = self.cv.fit_transform(self.df['TrimQuestion'])
		self.rankMatrix = pd.DataFrame(x.todense())
		self.rankMatrix.columns = self.cv.get_feature_names()
		self.vocabulary = self.cv.get_feature_names()

	def updateModel(self,index):
		self.df.loc[index,'PageRank'] = self.df['PageRank'][index] + 1

	def getLearningIndex(self,maxLength):
		val = int(input('\n Are you satisfied with which answer?')) 
		if val > maxLength or val <=0:
			print("Value you have entered is Invalid")
			return -1
		return val -1



	def printDetails(self,rankDict,maxAnswers=3):
		listQuestions = list(islice(rankDict,maxAnswers))
		listQuestions.sort(key= lambda x: self.df['PageRank'][x[0]], reverse=True)
		for i, question in enumerate(listQuestions):
			index = question[0]
			rank = rankDict[index]
			if rank ==0:
				break
			print(self.df['Question'][index])
			print(self.df['Answer'][index])
		if i == 0:
			print("Your Query doesn't match with any FAQ's. Try to contact our customer care")
			return
		learningIndex = getLearningIndex(len(listQuestions))

		if learningIndex != -1:
			index = listQuestions[learningIndex][0]
			print(self.df['Question'][index])
			print(self.df['Answer'][index])
			self.updateModel(index)



	def calculateRankforQuery(self,words,isReverse=True):
		sum = defaultdict(int)
		for i in range(0,len(self.df)):
			value =0
			for word in words:
				if word in self.vocabulary:
					value = value + self.rankMatrix[word][i]
			sum[i] = value
		return sorted(sum.items(), key=operator.itemgetter(1),reverse=isReverse)


	def search(self,query):
		queries = []
		queries.append(Lemmatizer.performLemmatization(query))
		x1 = self.cv.fit_transform(queries)
		words = self.cv.inverse_transform(x1)
		sorted_ranks = self.calculateRankforQuery(words[0],True)
		self.printDetails(sorted_ranks)
		

faqTrainer = DataTrainer(FAQ_DATA_SET,'\t')
faqTrainer.LoadDataSet()
faqTrainer.applyLemma()
faqTrainer.applyCV()
for i in range(2):
	query = input('\nEnter a query (dont use ? at the end): ')
	faqTrainer.search(query)



