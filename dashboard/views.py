from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login
from dashboard.models import *
from django.shortcuts import get_object_or_404





# Create your views here.
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
		print(request.POST)
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








	









	


