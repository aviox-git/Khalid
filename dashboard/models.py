from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import json


class Departments(models.Model):
	name = models.CharField(max_length=25)

class Employee(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	department = models.ForeignKey(Departments,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class Filemodel(models.Model):
	name = models.CharField(max_length=40)
	file = models.FileField(upload_to ='documents/', validators=[FileExtensionValidator(allowed_extensions=['xlsx','xls','xlt','xlm','xlsm','xltx','xltm','xlsb','xla','xlam','xll','xlw'])])
	
	def __str__(self):
		return self.name

class FileOjectModel(models.Model):
	file = models.ForeignKey(Filemodel,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length = 80)

	def __str__(self):
		return self.email

class TemplateModel(models.Model):
	name = models.CharField(max_length=40,blank = False)
	subject = models.CharField(max_length=100)
	body = models.TextField(blank = True,null = True)
	link = models.URLField(max_length=100,null = True,blank = True)
	apk_link = models.URLField(max_length=100,null = True,blank = True)
	ios_link = models.URLField(max_length=100,null = True,blank = True)
	html_template = models.CharField(max_length = 200, default = 'template1.html')

	def __str__(self):
		return self.name

class PromotionModel(models.Model):
	file = models.ForeignKey(Filemodel,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	start_on = models.DateField(blank=True, null=True)
	templates = models.ForeignKey(TemplateModel,on_delete=models.CASCADE,null= True)

	def __str__(self):
		return self.name 

user_choice =(('sent','sent'),('visited', 'visited'),('download','download'),('installed','installed'))		
class PromotionStatus(models.Model):
	promotion = models.ForeignKey(PromotionModel,on_delete=models.CASCADE, null =True)
	email_address = models.EmailField(max_length = 80)
	status = models.CharField(max_length = 20,choices = user_choice, default='sent')

user_choices =(('sent','sent'),('visited', 'visited'),('download','download'),('installed','installed'))	
FOR_REQUEST = (('ios','IOS'),('apk','APK'),('web','WEB'))	
class UserStatus(models.Model):
	promotion = models.ForeignKey(PromotionStatus, on_delete = models.CASCADE)
	status = models.CharField(max_length = 100, choices = user_choices, default='visited')
	ip_address = models.GenericIPAddressField()
	user_os = models.CharField(max_length = 450)
	visited_info = models.TextField(null = True)
	mobile_info = models.TextField(null = True)
	request_type = models.CharField(max_length = 5, choices = FOR_REQUEST)

	def visitedinfo(self):
		obj = json.loads(self.visited_info)
		print(obj,type(obj))
		return obj




