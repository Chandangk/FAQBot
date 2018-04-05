from bs4 import BeautifulSoup
import requests
import tsv

#writing tsv file
writer = open("C:\\Python27\\dataset.tsv", "w")
qid=1
writer.write("%s\t%s\t%s\t%s\n" % ("Question_id","Question","Answer","PageRank"))


#get soup obj
def getSoupObj(linkurl):
    innerResponse=requests.get(linkurl)
    innerData=innerResponse.text
    innerSoup=BeautifulSoup(innerData,'lxml')
    return innerSoup


#main logic
def qans(soup):
    questionClass=soup.findAll('div',{'class':'accordion'})
    for each_question in questionClass:
      questionArr=each_question.find('a').encode()
      answerTag=each_question.findAll('p')
      answer=""
      for each_answer in answerTag:
       if len(each_answer.getText()) > 1:
           answer+=each_answer.encode()
         # print("Answer:"+each_answer.getText())
      #print(questionArr+" "+answer)
      writer.write("%s\t%s\n" % (questionArr,answer))
      print("******************")
    return



#pagination logic
def pagination(soupObj):
    print("paginationcalled")
    pageTag=soupObj.find('ul',{'class':'pagination'})
    if(pageTag):
       pageATags=pageTag.findAll('a')
       for aTag in pageATags:
         if aTag.get('href'):
             formUrl=childUrl + aTag.get('href')
             print(formUrl)
             newObj=getSoupObj(formUrl)
             qans(newObj)
    return

#start
parentUrl="https://www.singaporeair.com/en_UK/faq/"
soup=getSoupObj(parentUrl)
childUrl=parentUrl[0:28]
print(childUrl)
divTag=soup.find('div',{'class':'inner'})
tags=divTag.find_all('a')
#iterating each links in main page
for tag in tags:
 formedUrl=childUrl + tag.get('href')
 print (formedUrl)
 soupObj=getSoupObj(formedUrl)
 qans(soupObj)
 pagination(soupObj)
 

writer.close() #close tsv file
