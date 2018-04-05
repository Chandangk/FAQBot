from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from AskFAQApp.itr import listitr
from AskFAQApp.models import DomainEntry,ServiceUrlMapping
from AskFAQApp.main import *

radioSelect=""
radio_1=""
radio_2=""
radio_3=""
#definig class for frequent questions
class Freq:

	def __init__(self,question,answer,pageRank=0):
		self.question=question
		self.answer=answer
		self.pageRank = pageRank

	def display(self):
		print("Question:"+self.question+" Answer:"+self.answer+"pageRank:"+self.pageRank)

	def getQuestion(self):
		return self.question



# Create your views here.
def index(request):
	return render(request,'index.html')

def detail(request,question):
	return HttpResponse("<h2>The question is"+str(question)+"</h2>")

def insertService(request,response):
	global serviceObject,serviceName,serviceFilePath,domainName,serviceUrl,domainObject
	result="ajax request made  but someother error"
	serviceNameGet=request.GET.get('serviceName')
	result=serviceNameGet
	if ServiceUrlMapping.objects.filter(serviceName=serviceNameGet).exists():
		result="Already exists!!!"
	else:
		domainNameGet=request.GET.get('domainName')
		serviceUrlGet=request.GET.get('serviceUrl')
		serviceObject=ServiceUrlMapping()
		filePath=serviceNameGet+".txt"
		status = createAndDownloadKB(serviceUrlGet,serviceNameGet,filePath)
		if status == 0:
			domainObject=DomainEntry.objects.get(domainName=domainNameGet)
			serviceObject.domainID=domainObject
			serviceObject.serviceName=serviceNameGet
			serviceObject.serviceCrawlerUrl=serviceUrlGet
			serviceObject.serviceFilePath=filePath
			serviceObject.save()
			result="Service saved successfully...."
		else:
			result="Problem in crawling..."
		return JsonResponse({"result":result})

def executor(request,response):
	global output_Value,filePath,domainName
	filePath=request.GET.get('serviceFilePath')
	domainName=request.GET.get('serviceName')
	print("executor called")
	return render(request,'index.html',{"domainName":domainName,"filePathVal":filePath})

def evaluation(request,response):
	global radio_1,radio_2,radio_3
	filePath=request.POST.get('filePath')
	question=request.POST.get('question_field')
	print("filepath is "+filePath)
	domainName=request.POST.get('domainName')
	output_value = search(filePath,question)
	print(output_value)
	if len(output_value) == 0:
		output_value+='.'+filePath+" "+domainName
	radio_1=output_value[0].questionId
	radio_2=output_value[1].questionId
	radio_3=output_value[2].questionId
	return render(request,'index.html',{"QAPairs":output_value,"question":question,"filePathVal":filePath})

def firstPage(request,response):
	domainObjects=DomainEntry.objects.all()
	serviceObjects=ServiceUrlMapping.objects.all()
	FreqList = getPopularFAQ()
	return render(request,'first.html',{"domainObj":domainObjects,"serviceObj":serviceObjects,"frequentList":FreqList})

def feedback(request,response):
	global selected_option1,selected_option2,selected_option3,radioSelect,radio_1,radio_2,radio_3
	feedback_value =0
	selected_option1=request.POST.get('optradio1')
	selected_option2=request.POST.get('optradio2')
	selected_option3=request.POST.get('optradio3')
	file_path = request.POST.get('filePathVal')
	print(selected_option1)
	if(selected_option1 == 'on'):
		radioSelect='1'
		feedback_value = int(radio_1)
	if(selected_option2 == 'on'):
		radioSelect='2'
		feedback_value = int(radio_2)
	if(selected_option3 == 'on'):
		radioSelect='3'
		feedback_value =int(radio_3)
	doReinforcement(feedback_value,file_path)
	return render(request,"index.html",{"radio_label":radioSelect})


def startPage(request,response):
	global name,filePath
	name=request.GET.get('serviceName')
	filePath=request.GET.get('serviceFilePath')
	return render(request,"index.html",{"serviceName":name,"filePathVal":filePath})


