from django.urls import path, include
from course import views


# 子路由模块
urlpatterns = [
    path('fbv/list/', views.course_list, name='fbv-list'),
    path('fbv/detail/<int:id>/', views.course_detail, name='fbv-detail')
]