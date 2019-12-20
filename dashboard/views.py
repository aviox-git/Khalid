from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login
from dashboard.models import *
from django.shortcuts import get_object_or_404
from dashboard.forms import *  
import os
from django.conf import settings
from django.http import HttpResponse, Http404
import datetime
import xlrd
from django.template import RequestContext


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def base(request):
	page = "homepage"
	return render(request,'dashboard/home.html',locals())


def login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		if password and username:
			user = authenticate(username = username,password = password)
			if user is not None:
				auth_login(request,user)
				messages.success(request, "You are successfully logged in")
				return HttpResponseRedirect("/dashboard")
			else:
				messages.error(request,'Invalid credentials')
				return HttpResponseRedirect('/dashboard/login')
	return render(request,'dashboard/login.html')

def logoutView(request):
	logout(request)
	messages.success(request,"you have successfully logged")
	return HttpResponseRedirect('/dashboard/login')

def department(request):
	page = "department"
	
	if request.method == 'POST':
		name = request.POST.get('name')
		Departments.objects.create(name = name)
		messages.success(request, "successfull")
		return HttpResponseRedirect('/dashboard/department')
		
	departments=Departments.objects.all()
	return render(request, 'dashboard/deparment.html',locals())

def departmentedit(request):
	if request.method == 'GET':
		dep_id = request.GET.get('id')
		department = Departments.objects.get(id=dep_id)
		department.delete()
		messages.error(request, 'Department is success deleted')
	if request.method == 'POST':
		dep_id = request.POST.get('id')
		name = request.POST.get('name')	
		department = Departments.objects.get(id=dep_id)
		department.name = name
		department.save()

	return HttpResponseRedirect('/dashboard/department')

def employees(request):
	page = "employees table"
	department = Departments.objects.all()
	emps = Employee.objects.all()
	if request.method == 'POST':
		
		employee_id = request.POST.get('id')
		data_emp = Employee.objects.get(id=employee_id)
		data_emp.delete() 
		messages.error(request, 'Employees is success deleted')

	
	return render(request,'dashboard/employees.html',locals())



def add_employees(request):
	page = "addemployees"
	dep = Departments.objects.all()
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email =  request.POST.get('email')
		image =  request.FILES.get('image')
		department_id = request.POST.get('department')
		password = request.POST.get("passwd")

		try:
			user = User.objects.get(username = email)
			messages.error(request , 'email already exist')
		except User.DoesNotExist:
			new_user = User(is_staff = True, first_name = first_name, last_name = last_name , username = email, email = email)
			new_user.set_password(password)
			new_user.save()
			employee_data = Employee(user = new_user, department_id = department_id)
			employee_data.save()
			messages.success(request , 'Username is successfully created')
		return HttpResponseRedirect('/dashboard/employees') 
	return render(request,'dashboard/addemployees.html',locals())


def employees_edit(request,emp_id):
	page = "edit employees"
	dep = Departments.objects.all()
	emp = Employee.objects.get(pk=emp_id)
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		department = request.POST.get('department')
		emp.user.first_name = first_name
		emp.user.last_name = last_name
		emp.user.save()

		depart = Departments.objects.get(pk=department)
		emp.department = depart
		emp.save()

		return HttpResponseRedirect('/dashboard/employees')

	return render(request,'dashboard/employees_edit.html',locals())



def active_employees(request, user_id):
	userid = user_id
	user = User.objects.get(id=userid)
	if user.is_active:
		user.is_active = False
		messages.error(request,'deactivated'.format(user.username))
	else:
		user.is_active = True
		messages.success(request,'user is active'.format(user.username))
	user.save()
	return HttpResponseRedirect('/dashboard/employees')	

  
def FileView(request):
	page = "event "
	file = Filemodel.objects.all()
	if request.method == 'POST':
		id = request.POST.get('id')
		data_file = Filemodel.objects.get(id=id)
		data_file.delete() 
		messages.error(request, 'Event  is success deleted')
	return render(request,'dashboard/fileview.html',locals()) 

		
def AddFile(request): 
	page = "add" 
	files= FileOjectModel.objects.all()
	if request.method == 'POST':
		file = FilemodelForm(request.POST, request.FILES)  	
		if file.is_valid():
			instance = file.save()
			book = xlrd.open_workbook(BASE_DIR  + instance.file.url)
			dict_list = []
			sheet = book.sheet_by_index(0)
			keys = sheet.row_values(0)
			obj_list = []
			for i in range(0, sheet.nrows):
				sheet.row_values(i)
				inputs=sheet.row_values(i)
				if len(inputs) == 2 and i != 0:
					name = inputs[0]
					email = inputs[1]
					obj_list.append(FileOjectModel(
											file = instance,
											name = name,
											email = email
											))
			FileOjectModel.objects.bulk_create(obj_list)		
		return HttpResponseRedirect("/dashboard/fileview")  
	else:  
		file = FilemodelForm()  
	return render(request,"dashboard/addfile.html",locals())  
		 
def File_edit(request, id):
	f_edit = Filemodel.objects.get(id=id) 
	if request.method == 'POST':
		form = FilemodelForm (request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/dashboard/fileview")
	else:
		form = FilemodelForm()  
	return render(request,"dashboard/file_edit.html",locals())  

def promotion(request):
	page ="promotion"
	prom = PromotionModel.objects.all()
	if request.method == 'POST':
		prom_id = request.POST.get('id')
		file = PromotionModel.objects.get(id=prom_id)
		file.delete() 
		messages.error(request, 'Promotion  is success deleted')

	return render(request,"dashboard/promotion.html",locals())  

def add_promotion(request):
	page = " new promotion"
	add_p = TemplateModel.objects.all()
	
	file = Filemodel.objects.all()
	if request.method == 'POST':
		name = request.POST.get('name')
		file = request.POST.get('file')
		start_on = request.POST.get('start_on')
		templates = request.POST.get('templates')

		file_model = Filemodel.objects.get(id=file)
		prom_model = TemplateModel.objects.get(id=templates)
		prom_add = PromotionModel(name = name , file = file_model, start_on = start_on, templates=prom_model)
		prom_add.save()
		messages.success(request,"Add Template successfull")
		return HttpResponseRedirect("/dashboard/promotion")
	return render(request,"dashboard/addpromotion.html", locals())

def promotion_edit(request,pk):
	page = "edit promotion"
	add_p = TemplateModel.objects.all()
	pros = Filemodel.objects.all()
	pro = PromotionModel.objects.get(pk=pk)
	if request.method == 'POST':
		a = request.POST.get('start_on')
		date = datetime.datetime.strptime(a, "%Y-%m-%d").date()
		name = request.POST.get('name')
		file = request.POST.get('file')
		templates = request.POST.get('templates')

		pro.name = name
		pro.start_on = date
		if file:
			file_obj = Filemodel.objects.get(pk = file)
			pro.file = file_obj
		
		if templates:
			file_prom = TemplateModel.objects.get(pk=templates)
			pro.templates = file_prom
		pro.save()



		return HttpResponseRedirect('/dashboard/promotion')
	return render(request,'dashboard/promotion_edit.html',locals())

def template(request):
	page = "templates"
	temp = TemplateModel.objects.all()
	if request.method =='POST':
		temp_id = request.POST.get('id')
		temps = TemplateModel.objects.get(id=temp_id)
		temps.delete()
		messages.success(request,"Template delete successfully")
	return render(request, 'dashboard/template.html', locals())


def add_template(request):
	adds= TemplateModel.objects.all()
	page = "template add"
	body= """Hi, 
	I am {{ Name}},
	here is my link {{ Link }}
	Thanks and regards.
	
	"""	
	if request.method == 'POST':
		name = request.POST.get('name')
		subject = request.POST.get('subject')
		body = request.POST.get('body')
		temp_add = TemplateModel(name = name , subject = subject, body = body)
		temp_add.save()
		messages.success(request,"Add Template successfull")
		return HttpResponseRedirect('/dashboard/template')

	return render(request, 'dashboard/addtemplate.html', locals())


def edit_template(request,pk):
	page = "edit template"

	temp_edit = TemplateModel.objects.get(pk=pk)
	if request.method == 'POST':
		name = request.POST.get('name')
		subject = request.POST.get('subject')
		body = request.POST.get('body')
		temp_edit.name = name
		temp_edit.subject = subject
		temp_edit.body = body
		temp_edit.save()
		
		messages.success(request,"Template Edit successfully")
		return HttpResponseRedirect('/dashboard/template')
		
	return render(request, 'dashboard/edit_template.html', locals())

def file_object(request,file_id):
	page = "file objects"
	file = FileOjectModel.objects.filter(file_id = file_id)
	if request.method == 'POST':
		file_id = request.POST.get('id')
		files = FileOjectModel.objects.get(id=file_id)
		file.delete()
		messages.success(request,"File objects delete successfully")

	return render (request,'dashboard/file_object.html', locals())


def object_add(request):
	page = "file add"
	add_obj = Filemodel.objects.all()
	file = FileOjectModel.objects.all()
	if request.method == 'POST':
		file = request.POST.get('file')
		name = request.POST.get('name')
		email = request.POST.get('email')
		add_temp = Filemodel.objects.get(id=file)
		add_temps =FileOjectModel(file = add_temp, name=name , email=email)
		add_temps.save()
		messages.success(request,"File object Added successfully")
		return HttpResponseRedirect('/dashboard/file-object')
	return render (request,'dashboard/object_add.html', locals())


def edit_object(request,pk):
	page = "edit object"
	obj_edit = Filemodel.objects.all()
	temp_edit = FileOjectModel.objects.get(pk=pk)
	if request.method == 'POST':

		file = request.POST.get('file')
		name = request.POST.get('name')
		email = request.POST.get('email')
		temp_edit.name = name
		temp_edit.email = email
		temp_edit.save()	
		file_obj = Filemodel.objects.get(id=file)
		temp_edit.file = file_obj
		temp_edit.save() 
		messages.success(request,"Template Edit successfully")
		return HttpResponseRedirect('/dashboard/file-object/'+str(file))
		
	return render(request, 'dashboard/edit_object.html', locals())



def mail(request,pk):
	page="mail"
	mails_data = PromotionModel.objects.get(pk=pk)
	subject = mails_data.templates.subject
	body = mails_data.templates.body
	file = mails_data.file
	email_list = list(FileOjectModel.objects.filter(file = file).values_list('email',flat=True))

	return HttpResponseRedirect('/dashboard/promotion')


















 



 








	









	


