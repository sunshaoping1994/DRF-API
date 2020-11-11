# 导入序列化模块
from rest_framework import serializers
from django import forms


# 导入模型类
from .models import Course
from django.contrib.auth.models import User


# 定义课程类
class CourseForm(forms.ModelForm):
    class Mate:
        model = Course
        fields = ('name', 'introduction', 'teacher', 'price')


# 定义用户类
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 数据包括所有
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # 外键字段，只读模式
    teacher = serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Course
        fields = '__all__'
        depth = 2


# class CourseSerializer(serializers.HyperlinkedRelatedField):
#     # 外键字段，只读模式
#     teacher = serializers.ReadOnlyField(source='teacher.username')
#
#     class Meta:
#         model = Course
#         # url是默认值
#         fields = ('id', 'url', 'name', 'introduction', 'teacher', 'price', 'create_time', 'update_time')