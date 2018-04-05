from __future__ import unicode_literals

from django.db import models

# Create your models here.
class FAQAppClass(models.Model):
	question=models.CharField(max_length=1000)
	answer=models.CharField(max_length=1000)


class DomainEntry(models.Model):
	domainID =models.AutoField(primary_key=True)
	domainName=models.CharField(max_length=250)

	def __str__(self):
		return str(self.domainID) + ' '+ self.domainName

class ServiceUrlMapping(models.Model):
	domainID=models.ForeignKey(DomainEntry,on_delete=models.CASCADE)
	serviceID=models.AutoField(primary_key=True)
	serviceName=models.CharField(max_length=250)
	serviceCrawlerUrl=models.CharField(max_length=250,default='dummyUrl')
	serviceFilePath=models.CharField(max_length=250)

	def __str__(self):
		return str(self.domainID.domainID)+ ' '+str(self.serviceID)+' '+self.serviceName+' '+self.serviceFilePath

	def checkEntry(serviceName):
		serviceObject=ServiceUrlMapping.objects.get()


class FrequentQuestions(models.Model):
	questionID=models.AutoField(primary_key=True)
	question=models.CharField(max_length=250)
	answer=models.CharField(max_length=250)


