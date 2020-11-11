"""drf_API URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # 获取Token接口
    path('api-token-auth', views.obtain_auth_token),
    # 管理员路由
    path('admin/', admin.site.urls),
    # DRF登录退出路由
    path('api-auth/', include('rest_framework.urls')),
    # 课程路由
    path('course/', include('course.urls')),
    # 获取API文档路由
    path('docs/', include_docs_urls(title='DRF API文档', description='DRF快速入门'))
]
