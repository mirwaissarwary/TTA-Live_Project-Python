################################################
# Imports

from django.forms import ModelForm
# from our models.py import our models
from .models import Report, UpdateReport

#################################################
# ModelForms


# Creates Report ModelForm based on Report Model...called by views.py
class ReportForm(ModelForm):
    # class Meta is used to change the behavior of the model fields like
    # changing order options,verbose_name, and a lot of other options
    class Meta:
        model = Report  # link to the model
        fields = '__all__'  # importing all the fields


# Creates UpdateReport ModelForm based on UpdateReport Model...called by views.py
class UpdateReportForm(ModelForm):
    class Meta:
        model = UpdateReport
        fields = '__all__'
