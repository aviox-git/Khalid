from django import forms  
from dashboard.models import * 
from django.contrib.admin.widgets import AdminDateWidget

class FilemodelForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/xlsx,xls,xlt,xlm,xlsm,xltx,xltm,xlsb,xla,xlam,xll,xlw'}))

    # file = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/.xls, .xlt, .xlm, .xlsx, .xlsm, .xltx, .xltm, .xlsb, .xla, .xlam, .xll, .xlw'}))
    class Meta:  
        model = Filemodel  
        fields = "__all__" 
 

class PromotionModelForm(forms.ModelForm):
	start_on = forms.DateField(input_formats='%Y-%m-%d')
	# date=forms.DateTimeField(help_text="blog date")

	class Meta:  
		model = PromotionModel  
		fields = "__all__"



