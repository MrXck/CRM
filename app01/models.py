from django.db import models
from django.utils.safestring import mark_safe
from multiselectfield import MultiSelectField
from rbac.models import Userinfo

# Create your models here.


course_choices = (
    ('LinuxL', 'Linux中高级'),
    ('PythonFullStack', 'Python高级全栈开发'),
)

class_type_choices = (
    ('fulltime', '脱产班'),
    ('online', '网络班'),
    ('weekend', '周末班'),
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

enroll_status_choices = (
    ('signed', '已报名'),
    ('unregistered', '未报名'),
    ('studying', '学习中'),
    ('pain_in_full', '学费已交齐'),
)

seek_status_choices = (
    ('A', '近期无报名计划'),
    ('B', '1月内报名'),
    ('C', '2周内报名'),
    ('D', '1周内报名'),
    ('E', '定金'),
    ('F', '到班'),
    ('G', '全款'),
    ('H', '无效'),
)

pay_type_choices = (
    ('deposit', '订金/报名费'),
    ('tuition', '学费'),
    ('transfer', '转班'),
    ('dropout', '退学'),
    ('refund', '退款'),
)

attendance_choices = (
    ('checked', '已签到'),
    ('vacate', '请假'),
    ('late', '迟到'),
    ('absence', '缺勤'),
    ('leave_early', '早退'),
)

score_choices = (
    (100, 'A+'),
    (90, 'A'),
    (85, 'B+'),
    (80, 'B'),
    (70, 'B-'),
    (60, 'C+'),
    (50, 'C'),
    (40, 'C-'),
    (0, 'D'),
    (-1, 'N/A'),
    (-100, 'COPY'),
    (-1000, 'FAIL'),
)


class Department(models.Model):
    name = models.CharField(max_length=12, verbose_name='部门名称')
    count = models.IntegerField(verbose_name='部门人数')


class UserInfo(Userinfo):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    email = models.EmailField()
    telephone = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)
    depart = models.ForeignKey('Department', default=1)

    def __str__(self):
        return self.username


class Customer(models.Model):
    qq = models.CharField('QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField('姓名', max_length=32, blank=True, null=True, help_text='学院报名后，请改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField('性别', choices=sex_type, max_length=16, default='male', blank=True, null=True)
    birthday = models.DateField('出生日期', default=None, help_text='格式yyyy-mm-dd', blank=True, null=True)
    phone = models.BigIntegerField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('self', verbose_name='转介绍自学员', blank=True, null=True, on_delete=models.CASCADE)
    course = MultiSelectField('咨询课程', choices=course_choices)
    class_type = models.CharField('班级类型', max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField('客户备注', blank=True, null=True)
    status = models.CharField('状态', choices=enroll_status_choices, max_length=64, default='unregistered', help_text='选择客户此时状态')
    date = models.DateTimeField('咨询日期', auto_now_add=True)
    last_consult_date = models.DateField('最后跟进日期', auto_now_add=True)
    next_date = models.DateField('预计再次跟进时间', blank=True, null=True)
    consultant = models.ForeignKey('UserInfo', verbose_name='销售', related_name='customers', blank=True, null=True, on_delete=models.CASCADE)
    class_list = models.ManyToManyField('ClassList', verbose_name='已报班级', blank=True)

    def __str__(self):
        return self.qq_name + ':' + self.qq

    def get_classlist(self):
        l = []
        for cls in self.class_list.all():
            l.append(str(cls))
        return mark_safe(','.join(l))

    def show_status(self):
        status_color = {
            'signed': 'yellow',
            'unregistered': 'red',
            'studying': 'lightblue',
            'pain_in_full': 'green',
        }
        return mark_safe(rf"<span style='color:{status_color[self.status]}'>{self.get_status_display()}</span>")


class ClassList(models.Model):
    course = models.CharField('课程名称', max_length=64, choices=course_choices)
    semester = models.IntegerField('学期')
    campuses = models.ForeignKey('Campuses', verbose_name='校区', on_delete=models.CASCADE)
    price = models.IntegerField('学费', default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField('开班日期')
    graduate_date = models.DateField('结业日期', blank=True, null=True)
    teachers = models.ForeignKey('UserInfo', verbose_name='老师', on_delete=models.CASCADE)
    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班级类型', blank=True, null=True)

    class Meta:
        unique_together = ('course', 'semester', 'campuses')

    def __str__(self):
        return f'{self.get_course_display()}{self.semester}({self.campuses})'


class Campuses(models.Model):
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class ConsultRecord(models.Model):
    customer = models.ForeignKey('Customer', verbose_name='所咨询客户')
    note = models.TextField(verbose_name='跟进内容...')
    status = models.CharField('跟进状态', max_length=8, choices=seek_status_choices, help_text='选择客户此时的状态')
    consultant = models.ForeignKey('UserInfo', verbose_name='跟进人', related_name='records')
    date = models.DateTimeField('跟进日期', auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    def __str__(self):
        return str(self.customer) + str(self.consultant)


class Enrollment(models.Model):
    why_us = models.TextField('为什么报名', max_length=1024, default=None, blank=True, null=True)
    your_expectation = models.TextField('学完想达到的具体期望', max_length=1024, blank=True, null=True)
    contract_approved = models.BooleanField('审批通过', help_text='在审阅完学员的资料无误后勾选此项，合同即生效', default=False)
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name='报名日期')
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    customer = models.ForeignKey('Customer', verbose_name='客户名称')
    school = models.ForeignKey('Campuses', verbose_name='校区')
    enrolment_class = models.ForeignKey('ClassList', verbose_name='所报班级')

    class Meta:
        unique_together = ('enrolment_class', 'customer')


class PaymentRecord(models.Model):
    pay_type = models.CharField('费用类型', choices=pay_type_choices, max_length=64, default='deposit')
    paid_fee = models.IntegerField('费用数额', default=0)
    note = models.TextField('备注', blank=True, null=True)
    date = models.DateTimeField('交款日期', auto_now_add=True)
    course = models.CharField('课程名', choices=course_choices, max_length=64, blank=True, null=True, default='N/A')
    class_type = models.CharField('班级类型', choices=class_type_choices, max_length=64, blank=True, null=True, default='N/A')
    enrolment_class = models.ForeignKey('ClassList', verbose_name='所报班级', blank=True, null=True)
    customer = models.ForeignKey('Customer', verbose_name='客户')
    consultant = models.ForeignKey('UserInfo', verbose_name='销售')
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    status_choice = (
        (1, '未审核'),
        (2, '已审核')
    )
    status = models.IntegerField(verbose_name='审核', default=1, choices=status_choice)
    confirm_date = models.DateTimeField(verbose_name='确认日期', null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name='确认人', to='UserInfo', related_name='confirms', null=True, blank=True)


class CourseRecord(models.Model):
    day_num = models.IntegerField('节次', help_text='此处填写第几节课或第几天课程...,必须为数字')
    date = models.DateField(auto_now_add=True, verbose_name='上课日期')
    course_title = models.CharField('本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField('本节课程内容', max_length=300, blank=True, null=True)
    has_homework = models.BooleanField(verbose_name='本节有作业', default=True)
    homework_title = models.CharField('本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField('作业描述', max_length=500, blank=True, null=True)
    scoring_point = models.TextField('得分点', max_length=300, blank=True, null=True)
    re_class = models.ForeignKey('ClassList', verbose_name='班级')
    teacher = models.ForeignKey('UserInfo', verbose_name='讲师')

    class Meta:
        unique_together = ('re_class', 'day_num')

    def __str__(self):
        return str(self.day_num)


class StudyRecord(models.Model):
    attendance = models.CharField('考勤', choices=attendance_choices, default='checked', max_length=64)
    score = models.IntegerField('本节成绩', choices=score_choices, default=-1)
    homework_note = models.CharField(max_length=255, verbose_name='作业批语', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField('备注', max_length=255, blank=True, null=True)
    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    course_record = models.ForeignKey('CourseRecord', verbose_name='某节课程')
    student = models.ForeignKey('Customer', verbose_name='学员')

    class Meta:
        unique_together = ('course_record', 'student')

    def __str__(self):
        return self.student.name + ':' + str(self.course_record.day_num)



