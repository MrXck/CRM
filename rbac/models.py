from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=12)
    permissions = models.ManyToManyField(to='Permission')

    def __str__(self):
        return self.name


class Userinfo(models.Model):
    # 如果有继承了这个类的类 那么 这个类里面的外键类需要 直接写类名
    # name = models.CharField(max_length=12)
    # password = models.CharField(max_length=32)
    roles = models.ManyToManyField(Role)  # 也就是这里需要直接写类 而不是 字符串 同时 关联的那个表 需要在这个类的上面

    class Meta:
        abstract = True  # 迁移数据库的时候不生成表


class Menu(models.Model):
    title = models.CharField(max_length=12, unique=True)
    icon = models.CharField(max_length=16, null=True, blank=True)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Permission(models.Model):
    url = models.CharField(max_length=64)
    title = models.CharField(max_length=32)
    menus = models.ForeignKey(to='Menu', null=True, blank=True, on_delete=models.CASCADE)
    parent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE)
    url_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.title



