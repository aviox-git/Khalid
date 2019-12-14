from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


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

class PromotionModel(models.Model):
	file = models.ForeignKey(Filemodel,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	start_on = models.DateField()

	def __str__(self):
		return self.name 
