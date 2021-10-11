

course_choices = (
    ('LinuxL', 'Linux中高级'),
    ('PythonFullStack', 'Python高级全栈开发'),
)

source_type = (
    ('qq', 'qq群'),
    ('referral', '内部转介绍'),
    ('website', '官网网站'),
    ('baidu_ads', '百度推广'),
    ('office_direct', '直接上门'),
    ('WoM', '口碑'),
    ('public_class', '公开课'),
    ('website_luffy', '路飞官网'),
    ('others', '其他')
)

sex_type = (
    ('male', '男'),
    ('female', '女')
)

# if __name__ == '__main__':
#     import os
#     import random
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
#     obj_list = []
#     import django
#     django.setup()
#     from app01 import models
#     for i in range(251):
#         d = {
#             'qq': '111111' + str(i),
#             'qq_name': '技师' + str(i) + '号',
#             'source': source_type[random.randint(0, 8)][0],
#             'course': course_choices[random.randint(0, 1)][0],
#             'sex': sex_type[random.randint(0, 1)][0]
#         }
#         obj = models.Customer(**d)
#         obj_list.append(obj)
#     models.Customer.objects.bulk_create(obj_list)
