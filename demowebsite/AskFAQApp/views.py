from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from itr import listitr
from AskFAQApp.models import DomainEntry,ServiceUrlMapping


#definig class for frequent questions
class Freq:

    def __init__(self,question,answer):
        self.question=question
        self.answer=answer

    def display(self):
        print("Question:"+self.question+" Answer:"+self.answer)

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
		domainObject=DomainEntry.objects.get(domainName=domainNameGet)
        serviceObject.domainID=domainObject
        serviceObject.serviceName=serviceNameGet
        serviceObject.serviceCrawlerUrl=serviceUrlGet
        serviceObject.serviceFilePath=filePath
        serviceObject.save()
        result="Service saved successfully...."

        return JsonResponse({"result":result})

def executor(request,response):
	global output_Value,filePath,domainName
	filePath=request.GET.get('serviceFilePath')
	domainName=request.GET.get('serviceName')
	return render(request,'index.html',{"domainName":domainName,"filePathVal":filePath})

def evaluation(request,response):
	question=request.POST.get('question_field')
	filePath=request.POST.get('filePath')
	domainName=request.POST.get('domainName')
	output_value=listitr(question)
	if output_value == "Not Found":
		output_value+='.'+filePath+" "+domainName

	return render(request,'index.html',{"output_Value":output_value,"question":question})

def firstPage(request,response):
	domainObjects=DomainEntry.objects.all()
	serviceObjects=ServiceUrlMapping.objects.all()
	FreqList= []
	FreqList.append(Freq("My ticket was purchased from a travel agent. Can I change my itinerary on singaporeair.com?","No, only tickets purchased on singaporeair.com or from a local Singapore .")) 
	FreqList.append(Freq("Am I eligible for online/mobile check-in?","Once you add someone"))
	FreqList.append(Freq("Why does Singapore Airlines charge a fee for booking","Yes  you ective links for more information"))
	FreqList.append(Freq("My ticket was purchased from a travel agent. Can I change my itinerary on singaporeair.com?","No, only tickets purchased on singaporeair.com or from a local Singapore .")) 
	FreqList.append(Freq("Am I eligible for online/mobile check-in?","Once yo them for six months."))
	FreqList.append(Freq("Why does Singapore Airlines charge a fee for bookings paid with credit cards?","Yes, you cann"))
	return render(request,'first.html',{"domainObj":domainObjects,"serviceObj":serviceObjects,"frequentList":FreqList})

def feedback(request,response):
	global selected_option1,selected_option2,selected_option3,radioSelect
	selected_option1=request.POST.get('optradi1')
	selected_option2=request.POST.get('optradi2')
	selected_option3=request.POST.get('optradi3')
	if(selected_option1 == 'on'):
		radioSelect='1'
	if(selected_option2 == 'on'):
		radioSelect='2'
	if(selected_option3 == 'on'):
		radioSelect='3'
	return render(request,"index.html",{"radio_label":radioSelect})


def startPage(request,response):
	global name,filePath
	name=request.GET.get('serviceName')
	filePath=request.GET.get('serviceFilePath')
	return render(request,"index.html",{"serviceName":name,"filePathVal":filePath})


