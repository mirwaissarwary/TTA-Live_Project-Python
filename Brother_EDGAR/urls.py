from django.urls import path
from . import views


# Creating necessary URL paths
urlpatterns = [
    path('home/', views.be_home, name='BrotherEDGAR_home'),
    path('create/', views.be_create, name='be_create'),
    path('displayReport/<int:pk>', views.be_displayReport, name='be_displayReport'),
    path('updateReport/<int:pk>', views.be_updateReport, name='be_updateReport'),
    path('deleteReport/<int:pk>', views.be_deleteReport, name='be_deleteReport'),
    path('searchPage/<int:pk>', views.be_searchPage, name='be_searchPage'),
    path('yahooFinance/<int:pk>', views.be_yahooFinance, name='be_yahooFinance'),
]
