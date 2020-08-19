from django.contrib import admin
from django.urls import path,include

from apptang import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pachong/',views.fun_method2),
]