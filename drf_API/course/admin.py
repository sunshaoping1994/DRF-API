from django.contrib import admin
from .models import Course


# list_display即要显示的数据
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'introduction', 'teacher', 'price')
    # 可以搜索的字段
    search_fields = list_display
    # 可以过滤的字段
    list_filter = list_display