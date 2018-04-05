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
import urllib
import io
import requests
import json
import os

FAQ_DATA_SET = 'dataset.txt'
faqTrainer = None
DataSets = {}


class FAQSet(object):
	"""docstring for FAQSet"""             
	def __init__(self, questionId,question,answer,pageRank=0):
		self.questionId = questionId
		self.question = question
		self.answer = answer
		self.pageRank = pageRank


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
		print("Updated index: "+str(index))

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


	def constrcutResult(self,rankDict,maxAnswers=3):
		retVal = []
		listQuestions = list(islice(rankDict,maxAnswers))
		listQuestions.sort(key= lambda x: self.df['PageRank'][x[0]], reverse=True)
		for i, question in enumerate(listQuestions):
			index = question[0]
			rank = rankDict[index]
			if rank ==0:
				break
			faq = FAQSet(index,self.df['Question'][index],self.df['Answer'][index])
			retVal.append(faq)
		if i == 0:
			print("Your Query doesn't match with any FAQ's. Try to contact our customer care")
		return retVal



	def searchInDB(self,query):
		print("search called query is "+ query)
		queries = []
		queries.append(Lemmatizer.performLemmatization(query))
		x1 = self.cv.fit_transform(queries)
		words = self.cv.inverse_transform(x1)
		sorted_ranks = self.calculateRankforQuery(words[0],True)
		return self.constrcutResult(sorted_ranks)
		

#def onLoad():
##	faqTrainer = DataTrainer(FAQ_DATA_SET,'\t')
#	faqTrainer.LoadDataSet()
#	faqTrainer.applyLemma()
#	faqTrainer.applyCV()


def search(fileName,query):
	global faqTrainer
	print("search called with params "+ str(fileName) + str(query))
	faqTrainer = getDataTrainer(fileName)
	return faqTrainer.searchInDB(query)
	
def doReinforcement(index,fileName,sep='\t'):
	global faqTrainer
	if faqTrainer is None:
		faqTrainer = getDataTrainer(fileName,sep)
	print ("Index: " +str(index))
	faqTrainer.updateModel(index)
	setDataTrainer(fileName,faqTrainer)

def setDataTrainer(fileName,faqTrainer):
	global DataSets
	DataSets[fileName] = faqTrainer

def getDataTrainer(fileName,sep='\t'):
	global DataSets
	print("getDataTrainer called..")
	if fileName not in DataSets:
		dataSet = loadFromDisk(fileName,sep)
		dataSet.applyLemma()
		dataSet.applyCV()
		DataSets[fileName] = dataSet
	return DataSets[fileName]

def loadFromDisk(fileName,sep='\t'):
	print("loadFromDisk called "+ fileName)
	dataSet = DataTrainer(fileName,sep)
	dataSet.LoadDataSet()
	return dataSet
def getKBId(urlToRequest, nameOfTheApp):

	if type(urlToRequest )is not list:
		urlArray  = []
		urlArray.append(urlToRequest)
	else:
		urlArray = urlToRequest


	url = 'https://westus.api.cognitive.microsoft.com/qnamaker/v2.0/knowledgebases/create' 
	data = {
	"name" : nameOfTheApp,
	"qnaPairs": [],
	"urls": urlArray }
	headers = {'Content-type': 'application/json', 'Ocp-Apim-Subscription-Key': 'b50bd4ee90ae4e6ca557930911b53ed2'}
	r = requests.post(url, data=json.dumps(data), headers=headers)

	response = r.json()
	if(r.status_code == 201):
		print(response)
		return response['kbId']
	return ""

def download(kbId,fileName):
		print("received kbId "+ kbId)
		if(len(kbId) ==0):
			print("invalid kbid received.."+kbId)
			return -1
		url = 'https://westus.api.cognitive.microsoft.com/qnamaker/v2.0/knowledgebases/%s' %kbId
		headers = {'Ocp-Apim-Subscription-Key': 'b50bd4ee90ae4e6ca557930911b53ed2'}
		r = requests.get(url, headers=headers)
		print(r.content)
	
		s=requests.get(r.content[1:-1]).content
		#print(s)
		df=pd.read_csv(io.StringIO(s.decode('utf-8')),sep='\t')
		df['Question_id'] = range(1, len(df) + 1)
		df['PageRank'] =0
		cols = ['Question_id','Question','Answer','PageRank','Source']
		df = df[cols]
		df.head()
		df.to_csv(fileName, sep='\t', encoding='utf-8')
		return 0

def createAndDownloadKB(urlToRequest,nameOfTheApp,fileName):
	print ("create and download kb called()...")
	kbId = getKBId(urlToRequest,nameOfTheApp)
	if len(kbId) <10:
		return -1
	else:
		return download(kbId,fileName)

def getPopularFAQ(maxCount = 10 ):
	print("getPopularFAQ called")
	popular_list = []
	files = os.listdir()
	files_txt = [i for i in files if i.endswith('.txt')]
	print("No of files found "+ str(len(files_txt)))
	data_frames = []
	df =pd.DataFrame()
	for file_name in files_txt:
		faqTrainer = getDataTrainer(file_name)
		df = df.append(faqTrainer.df)
	if len(files_txt) != 0:
		df = df.sort_values(by=['PageRank'], ascending=False)
		df2 = df.head(maxCount)
		for index, row in df2.iterrows():
			popular_list.append(FAQSet(index,row['Question'],row['Answer'],row['PageRank']))
	return popular_list
		











