# DRF视图开发RESTful API接口
# 1、函数式编程 Function Based View
# 2、类视图 Classed Based View
# 3、通用类视图 Generic Classed Based View
# 4、DRF的视图集viewsets
# 接口函数的分页，排序，认证，权限，限流等功能


import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
#
#
# course_dict = {
#     'name': '课程名称',
#     'introduction': '课程介绍',
#     'price': 0.11
# }
#
#
# # Django函数式编程(Django FRV 编写API接口)
# # 取消csrf限制
# @csrf_exempt
# def course_list(request):
#     if request.method == 'get':
#         return JsonResponse(course_dict)
#
#     if request.method == 'post':
#         course = json.load(request.body.decode('utf-8'))
#         return HttpResponse(json.dumps(course), content_type='application/json')
#
#
# # Django类视图（Django CVB 编写API接口）
# # 当http中的request请求进入的时候，先找到dispatch，然后再分发到get或者post中
# @method_decorator(csrf_exempt, name='dispatch')
# class CourseList(View):
#
#     def get(self, request):
#         return JsonResponse(course_dict)
#
#     def post(self, request):
#         course = json.loads(request.body.decode('utf-8'))
#         return HttpResponse(json.dumps(course), content_type='application/json')
# 视图装饰器
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# 返回数据
from rest_framework.response import Response
# 状态码及解释
from rest_framework import status
# 导入模型类
from .models import Course
from .serializers import CourseSerializer
# 用户保存之后再触发函数
from django.db.models.signals import post_save
# 接受信号函数
from django.dispatch import receiver
# 导入Django的用户模型类
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerReadOnly
from rest_framework import generics


# 装饰器
@receiver(post_save, sender=settings.AUTH_USER_MODEL)   # Django的信号机制
def generate_token(sender, instance=None, created=False, **kwargs):
    """
    创建用户时自动生成Token
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        # 新建用户Token
        Token.objects.create(user=instance)


"""
一、函数式编程Function Based View
"""
# 装饰器（用于装饰后面的方法）
@api_view(['GET', 'POST'])
# 使用装饰器，同时验证基本验证，Session验证，Token验证
@authentication_classes((BasicAuthentication, SessionAuthentication, TokenAuthentication))
# 使用装饰器验证只有登录用户才能操作权限，只有对象所有者才能编辑权限
@permission_classes((IsAuthenticated, IsOwnerReadOnly))
def course_list(request):
    """
    获取所有课程或者新增一个课程
    :param request:
    :return:
    """
    if request.method == 'GET':
        s = CourseSerializer(instance=Course.objects.all(), many=True)
        # 将数据数列化后传送到前端
        return Response(data=s.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # 将前端传送数据反数列化，partial允许前端数据局部更新
        s = CourseSerializer(data=request.data, partial=True)
        # 校验数据是否正确
        if s.is_valid():
            s.save(teacher=request.user)
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        # 不正确即返回错误信息到前端
        return Response(s.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((BasicAuthentication, SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, IsOwnerReadOnly))
def course_detail(request, id):
    """
    获取一个课程信息，更新删除课程信息
    :param request:
    :param id:
    :return:
    """
    try:
        # 通过前端id查询课程数据
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response(data={'msg': '无此课程信息'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # 根据id查询课程信息
        if request.method == 'GET':
            s = CourseSerializer(instance=course)
            return Response(data=s.data, status=status.HTTP_200_OK)

        # 根据id更改课程信息
        elif request.method == 'PUT':
            # 前端数据传入后台
            s = CourseSerializer(instance=course, data=request.data)
            # 验证数据
            if s.is_valid():
                s.save()
                return Response(s.data, status=status.HTTP_200_OK)

        # 根据id删除课程信息
        elif request.method == 'DELETE':
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


"""
三、通用类视图
"""


class GCourseList(generics.ListCreateAPIView):
    """
    获取课程列表，内置方法
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class GCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    更新课程列表，内置方法
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)
