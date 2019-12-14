from django.urls import path,include
from dashboard import views
app_name='dashboard'

urlpatterns = [
	path('', views.base, name='home'),
	path('layout', views.layout, name='layout'),
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





	# path('fileview/', views.download, name='fileview'),

    # path('show',views.show, name='show'),  
    # path('edit/<int:id>', views.edit),  
    # path('update/<int:id>', views.update),  
    # path('delete/<int:id>', views.destroy), 
 



    # path('department/?P<id>\d+)', views.department, name='department'),



	
]