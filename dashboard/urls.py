from django.urls import path,include
from dashboard import views

app_name='dashboard'

urlpatterns = [
	path('', views.base, name='home'),
	
	path('login', views.login, name='login'),
	path('dashboard_logout', views.logoutView, name='dashboard_logout'),

	path('department/', views.department, name='department'),
	path('department-edit', views.departmentedit, name='department_edit'),

	path('employees/', views.employees, name='employees'),
	path('addemployees', views.add_employees, name='addemployees'),
	path('employees-edit/<int:emp_id>', views.employees_edit, name='employees-edit'),
	path('activeemployees/<int:user_id>/',views.active_employees , name="activeemployees"),

	path('fileview/', views.FileView, name='fileview'),
	path('addfile/', views.AddFile, name='addfile'),
	path('file-edit/<int:id>', views.File_edit, name='file_edit'),

	path('promotion/', views.promotion, name='promotion'),
	path('addpromotion/', views.add_promotion, name = 'addpromotion'),
	path('promotion-edit/<int:pk>', views.promotion_edit, name='promotion_edit'),
	path('mail/<int:pk>', views.mail,name='mail'),

	path('template/', views.template, name='template'),
	path('addtemplate/', views.add_template, name = 'addtemplate'),
	path('edit-template/<int:pk>', views.edit_template, name = 'edit_template'),

	path('file-object/<int:file_id>', views.file_object, name='file_object'),
	path('object-add/', views.object_add, name= 'object_add'),
	path('edit-object/<int:pk>', views.edit_object, name='edit_object'),

	path('update',views.UpdateUser.as_view(),name="update"),
	path('results/<int:prom_id>', views.results,name="results"),
	path('details/<int:prom_id>', views.Details,name="details"),
	path('template1', views.template1,name="template1"),
	path('template2', views.template2,name="template2"),
	path('template3', views.template3,name="template3"),
	path('template4', views.template4,name="template4"),

	path('send_again', views.send_again,name="send_again"),
	path('upload', views.upload,name="upload"),

	path('users', views.users,name="users"),
]