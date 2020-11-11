from rest_framework import permissions


class IsOwnerReadOnly(permissions.BasePermission):
    """
    自定义权限，只允许对象的所有者能够编辑，重写permissions源码方法
    """
    def has_object_permission(self, request, view, obj):
        """
        所有request请求都有读权限，因此允许GET/HEAD/OPTIONS方法
        :param request:
        :param view:
        :param obj:
        :return:
        ('GET', 'HEAD', 'OPTIONS')==permissions.SAFE_METHODS(源码自定义变量)
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        # 对象所有者才能编辑权限
        return obj.teacher == request.user
