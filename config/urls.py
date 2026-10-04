"""URL routes for the Brother EDGAR-only slice."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/Brother_EDGAR/home/', permanent=False)),
    path('Brother_EDGAR/', include('Brother_EDGAR.urls')),
]
