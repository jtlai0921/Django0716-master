"""Django0716 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
import Django0716.views as views
#from Django0716.views import hello, hello_name, hello_add, hello2_add

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('hello/<str:name>/', views.hello_name),
    path('hello/add/<int:x>/<int:y>/', views.hello_add),  # http://127.0.0.1:8000/hello/add/100/200/
    path('hello2/add/', views.hello2_add),                # http://127.0.0.1:8000/hello2/add/?x=100&y=200

    path('hello_template/', views.hello_template),
    path('hello_template/<str:name>/', views.hello_template_name),
    path('hello_template_users/', views.hello_template_users),

    path('fruit_form/', views.fruit_form),
    path('fruit_result/', views.fruit_result),

    path('youbike_form/', views.youbike_form),
    path('youbike_result/', views.youbike_result),
    path('map/', views.map),

    path('login_form/', views.login_form),
    path('login_result/', views.login_result),

    path('macdonald_form/', views.macdonald_form),
    path('macdonald_result/', views.macdonald_result),
    path('macdonald_clear/', views.macdonald_clear),
    path('login_session/', views.login_session),
    path('login_session_check/', views.login_session_check),
    path('login_session_out/', views.login_session_out),

    path('ajax_lotto_form/', views.ajax_lotto_form),
    path('ajax_lotto_result/', views.ajax_lotto_result),

    path('ajax_rating_form/', views.ajax_rating_form),
    path('ajax_rating_result/', views.ajax_rating_result),

    # captcha
    path('captcha/', include('captcha.urls')),
    path('user_login_form/', views.user_login_form),
    path('user_login/', views.user_login),
    path('user_logout/', views.user_logout),
    path('user_crud_form/', views.user_crud_form),

]
