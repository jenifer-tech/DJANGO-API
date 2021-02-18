"""prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from account.views import(
	registration_view,
	account_properties_view,
	update_account_view,
    ObtainAuthTokenView,
)
app_name = 'account'
urlpatterns = [
    path('admin/', admin.site.urls),
	path('history/', account_properties_view, name="properties"),
	path('history/update', update_account_view, name="update"),
	path('login', ObtainAuthTokenView.as_view(), name="login"), 
	path('register', registration_view, name="register"),
]



