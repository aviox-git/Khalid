from django.db import models
from django.contrib.auth.models import User
class Departments(models.Model):
	name = models.CharField(max_length=25)

class Employee(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	department = models.ForeignKey(Departments,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username








