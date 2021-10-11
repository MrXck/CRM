from django.contrib import admin
from app01 import models
from rbac.models import Permission, Menu, Role
# Register your models here.


admin.site.register(models.UserInfo)
admin.site.register(models.Campuses)
admin.site.register(models.Customer)
admin.site.register(models.ClassList)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
admin.site.register(models.CourseRecord)
admin.site.register(Menu)
admin.site.register(Role)
admin.site.register(Permission)


"""
    superuser: xck
    password: xcknbplus
"""
