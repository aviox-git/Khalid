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
from Khalid.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import string 
import random
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PromotionSerialiser
from django.contrib.auth.decorators import login_required
from user_agents import parse
from django.template import loader
import ipinfo
from django.db.models import Q
from django.core.files.storage import default_storage


access_token = 'dbeef9181999dc'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

login_url = '/login'


class promotionlist(APIView):

	def get(self,request):
		promotion1 = PromotionModel.objects.all()
		serializer = PromotionSerialiser(promotion1, many = True)
		return Response(serializer.data)

	def post(self, request):
		serializer = PromotionSerialiser(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url = login_url)
def base(request):
	page = "homepage"
	return render(request,'dashboard/home.html',locals())

def layout(request):
	return render(request,'dashboard/layout.html')


def login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		if password and username:
			user = authenticate(username = username,password = password)
			if user is not None:
				auth_login(request,user)
				messages.success(request, "You are successfully logged in")
				return HttpResponseRedirect("/")
			else:
				messages.error(request,'Invalid credentials')
				return HttpResponseRedirect('/login')
	return render(request,'dashboard/login.html')

@login_required(login_url = login_url)
def logoutView(request):
	logout(request)
	messages.success(request,"you have successfully logged")
	return HttpResponseRedirect('/login')

@login_required(login_url = login_url)
def department(request):
	page = "department"
	
	if request.method == 'POST':
		name = request.POST.get('name')
		Departments.objects.create(name = name)
		messages.success(request, "successfull")
		return HttpResponseRedirect('/department')
		
	departments=Departments.objects.all()
	return render(request, 'dashboard/deparment.html',locals())

@login_required(login_url = login_url)
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

	return HttpResponseRedirect('/department')

@login_required(login_url = login_url)
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

@login_required(login_url = login_url)
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
		return HttpResponseRedirect('/employees') 
	return render(request,'dashboard/addemployees.html',locals())

@login_required(login_url = login_url)
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

		return HttpResponseRedirect('/employees')

	return render(request,'dashboard/employees_edit.html',locals())


@login_required(login_url = login_url)
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
	return HttpResponseRedirect('/employees')	

@login_required(login_url = login_url) 
def FileView(request):
	page = "Files "
	file = Filemodel.objects.all()
	if request.method == 'POST':
		id = request.POST.get('id')
		data_file = Filemodel.objects.get(id=id)
		data_file.delete() 
		messages.error(request, 'Event  is success deleted')
	return render(request,'dashboard/fileview.html',locals()) 

@login_required(login_url = login_url)		
def AddFile(request): 

	
	# if request.method == 'POST':  
	# 	file = FilemodelForm(request.POST, request.FILES)  
	# 	if file.is_valid():
	# 		file.save()
	# 		return HttpResponseRedirect("/dashboard/fileview")


	page = "add CSV File" 
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
			return HttpResponseRedirect("/fileview") 
		else:
			if file.errors:
				for field in file:
					for error in field.errors:
						messages.error(request,"{} in  {}".format(error,field.name)) 

	else:  
		file = FilemodelForm()  
	return render(request,"dashboard/addfile.html",locals())  

@login_required(login_url = login_url)		 
def File_edit(request, id):
	page = "edit file"
	f_edit = Filemodel.objects.get(id=id) 
	if request.method == 'POST':
		form = FilemodelForm (request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/fileview")
		else:
			if form.errors:
				for field in form:
					for error in field.errors:
						messages.error(request,"{} in  {}".format(error,field.name))
	else:
		form = FilemodelForm()  
	return render(request,"dashboard/file_edit.html",locals())  



def promotion(request):
	
	# print(request.META)
	page ="promotion"
	prom = PromotionModel.objects.all()
	if request.method == 'POST':

		prom_id = request.POST.get('id')
		file = PromotionModel.objects.get(id=prom_id)
		file.delete() 
		messages.error(request, 'Promotion  is success deleted')

	return render(request,"dashboard/promotion.html",locals())  

@login_required(login_url = login_url)
def add_promotion(request):

	page = "Add promotion"
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
		return HttpResponseRedirect("/promotion")
	return render(request,"dashboard/addpromotion.html", locals())

@login_required(login_url = login_url)
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
		return HttpResponseRedirect('/promotion')
	return render(request,'dashboard/promotion_edit.html',locals())

@login_required(login_url = login_url)
def template(request):
	page = "templates"
	temp = TemplateModel.objects.all()
	if request.method =='POST':
		temp_id = request.POST.get('id')
		temps = TemplateModel.objects.get(id=temp_id)
		temps.delete()
		messages.success(request,"Template delete successfully")
	return render(request, 'dashboard/template.html', locals())

@login_required(login_url = login_url)
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
		link = request.POST.get('link')
		app_link = request.POST.get('app_link')
		ios_link = request.POST.get('ios_link')

		temp_add = TemplateModel(name = name , subject = subject, body = body, link=link)
		temp_add.apk_link = app_link
		temp_add.ios_link = ios_link
		temp_add.save()
		messages.success(request,"Add Template successfull")
		return HttpResponseRedirect('/template')

	return render(request, 'dashboard/addtemplate.html', locals())

@login_required(login_url = login_url)
def edit_template(request,pk):
	page = "edit template"

	if not request.user.is_superuser:
		messages.error(request, 'You dont have the access of it')
		return HttpResponseRedirect('/')
	temp_edit = TemplateModel.objects.get(pk=pk)
	if request.method == 'POST':
		name = request.POST.get('name')
		subject = request.POST.get('subject')
		body = request.POST.get('body')
		link = request.POST.get('link')
		apk_link = request.POST.get('app_link')
		ios_link = request.POST.get('ios_link')
		ajax = request.POST.get('ajax')

		if ajax:
			html = request.POST.get('html')
			temp_edit.body = html
			temp_edit.save()
			return HttpResponse({})

		temp_edit.name = name
		temp_edit.subject = subject
		temp_edit.link = link
		temp_edit.apk_link = apk_link
		temp_edit.ios_link = ios_link
		temp_edit.save()
		
		messages.success(request,"Template Edit successfully")
		return HttpResponseRedirect('/template')
		
	return render(request, 'dashboard/edit_template.html', locals())

@login_required(login_url = login_url)
def file_object(request,file_id):
	page = "file objects"
	file = FileOjectModel.objects.filter(file_id = file_id)
	if request.method == 'POST':
		file_id = request.POST.get('id')
		files = FileOjectModel.objects.get(id=file_id)
		file.delete()
		messages.success(request,"File objects delete successfully")
		return HttpResponseRedirect('/file-object/'+str(file_id))

	return render (request,'dashboard/file_object.html/', locals())

@login_required(login_url = login_url)
def object_add(request):
	page = "add objects"
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
		return HttpResponseRedirect('/file-object/'+str(file))
	return render (request,'dashboard/object_add.html', locals())

@login_required(login_url = login_url)
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
		return HttpResponseRedirect('/file-object/'+str(file))
		
	return render(request, 'dashboard/edit_object.html', locals())

@login_required(login_url = login_url)
def mail(request,pk):
	
	mails_data = PromotionModel.objects.get(pk=pk)
	subject = mails_data.templates.subject
	file = mails_data.file
	email_list = list(FileOjectModel.objects.filter(file = file).values_list('email',flat=True))
	

	for item in email_list:
		res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 8))
		promotion_status = PromotionStatus(email_address=item , promotion=mails_data)
		promotion_status.save()
		link = 'https://nehjezdoor.online/' + 'download/' + res + str(promotion_status.id)
		temp_obj = mails_data.templates
		site = 'https://nehjezdoor.online'
		html_message = loader.render_to_string('dashboard/'+ mails_data.templates.html_template,locals())
		html_message = html_message.replace('http://vikasaviox123',link)
		message = "Hello User"
		send_mail(subject, message, (mails_data.name).upper(), [item,],html_message = html_message)
	messages.success(request,"Email sent successfully")

	return HttpResponseRedirect('/promotion',locals())

def download(request,slug):

	slices = int(slug[8:])
	type_ = request.GET.get('type')
	status_id = PromotionStatus.objects.get(id=slices)
	status_id.status ="visited"
	status_id.save()
	handler = ipinfo.getHandler(access_token)
	# details = handler.getDetails(request.META.get('REMOTE_ADDR'))
	details = handler.getDetails()

	user = UserStatus(
		promotion = status_id,
		status = status_id.status, 
		ip_address = request.META.get('REMOTE_ADDR'),
		user_os = request.META.get('HTTP_USER_AGENT'),
		)
	visited_info = json.dumps(details.all)

	user.visited_info = json.dumps(details.all)
	
	if type_ == 'web':
		user.request_type = 'web'
		link = status_id.promotion.templates.link
	elif type_ == 'ios':
		user.request_type = 'ios'
		link = status_id.promotion.templates.ios_link
	elif type_ == 'apk':
		user.request_type = 'apk'
		link = status_id.promotion.templates.apk_link
	if "google-proxy" not in visited_info:
		user.save()
	return HttpResponseRedirect(link)

class UpdateUser(APIView):

	def post(self,request):

		get_ip = request.META.get('REMOTE_ADDR')
		get_from_post = request.POST.get('ip')
		device_info =  request.POST.get('device_info')
		response = {}
		try:
			try:
				user_obj = UserStatus.objects.filter(Q(ip_address = get_ip , status = 'visited',mobile_info__isnull = True), (Q(request_type = 'ios')| Q(request_type = 'apk'))).latest('-pk')
			except Exception as e:
				user_obj = UserStatus.objects.filter(ip_address = get_ip , status = 'visited',mobile_info__isnull = True).latest('-pk')

			finally:
				
				if user_obj:
					user_obj.status = 'installed' 
					user_obj.ip_address = request.META.get('REMOTE_ADDR')
					handler = ipinfo.getHandler(access_token)
					details = handler.getDetails(request.META.get('REMOTE_ADDR'))
					details_dict = {}
					details_dict.update(request.data)
					details_dict.update(details.all)
					user_obj.mobile_info = json.dumps(details_dict)
					user_obj.promotion.status = 'installed'
					user_obj.promotion.save()
					user_obj.save()
					response['status'] = 200
		except Exception as e:
			pass

		return Response(response)

@login_required
def results(request,prom_id):
	page = "View Promotion results"
	promotion_id = prom_id
	promotions = PromotionStatus.objects.filter(promotion_id = prom_id)
	return render(request,'dashboard/results.html',locals())

@login_required
def template1(request):
	temp = request.GET.get('id')
	if temp:
		link = "http://vikasaviox123"
		site = 'https://nehjezdoor.online'
		temp_obj = TemplateModel.objects.get(id= temp)
	return render(request,'dashboard/template1.html',locals())

@login_required
def template2(request):
	temp = request.GET.get('id')
	if temp:
		link = "http://vikasaviox123"
		site = 'https://nehjezdoor.online'
		temp_obj = TemplateModel.objects.get(id= temp)
	return render(request,'dashboard/template2.html',locals())

@login_required
def template3(request):
	temp = request.GET.get('id')
	if temp:
		link = "http://vikasaviox123"
		site = 'https://nehjezdoor.online'
		temp_obj = TemplateModel.objects.get(id= temp)
	return render(request,'dashboard/template3.html',locals())

@login_required
def template4(request):
	temp = request.GET.get('id')
	if temp:
		link = "http://vikasaviox123"
		site = 'https://nehjezdoor.online'
		temp_obj = TemplateModel.objects.get(id= temp)
	return render(request,'dashboard/template4.html',locals())

def Details(request,prom_id):
	page = "View User Results"
	userinfo = UserStatus.objects.filter(promotion_id = prom_id)
	return render(request,'dashboard/details.html',locals())

def send_again(request):
	response = {}
	if request.method == 'POST':
		data_id = request.POST.getlist('data_ids[]')
		promotion_id = request.POST.get('promotion_id')
		mails_data = PromotionModel.objects.get(pk=promotion_id)
		promotion = PromotionStatus.objects.filter(pk__in = data_id)
		subject = mails_data.templates.subject
		file = mails_data.file

		for promotion_status in promotion:

			res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 8))
			promotion_status.status = 'sent'
			link = 'https://nehjezdoor.online/' + 'download/' + res + str(promotion_status.id)
			temp_obj = mails_data.templates
			site = 'https://nehjezdoor.online'
			html_message = loader.render_to_string('dashboard/'+ mails_data.templates.html_template,locals())
			html_message.replace('http://vikasaviox123',link)
			message = "Hello"

			send_mail(subject, message, (mails_data.name).upper(), [promotion_status.email_address,],html_message = html_message)
			promotion_status.save()
			response['status'] = True
	return HttpResponse(json.dumps(response) , content_type = 'application/json')

def upload(request):
	if request.method == 'POST':
		file = request.FILES.get('file')
		if file:
			file_name = default_storage.save('images/'+ file.name, file)
			url = '/media/images/' + file.name
		return HttpResponse(url)

def users(request):
	users = UserStatus.objects.all().order_by('promotion')
	return render(request,'dashboard/user_result.html',locals())







 