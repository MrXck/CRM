from django import forms
from app01 import models

from django.forms.fields import DateField


class CustomerForm(forms.ModelForm):

    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for file_name, field in self.fields.items():
            if file_name == 'course':
                continue
            if isinstance(field, DateField):
                field.widget.attrs.update({'type': 'date'})
            field.widget.attrs.update({'class': 'form-control'})


class ConsultRecordForm(forms.ModelForm):

    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status', ]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for file_name, field in self.fields.items():
            if file_name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant_id=request.user_obj.pk)
            elif file_name == 'consultant':
                field.choices = ((request.user_obj.pk,
                                  models.UserInfo.objects.filter(id=request.user_obj.pk).first().username), )
            field.widget.attrs.update({'class': 'form-control'})


class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = models.Enrollment
        fields = '__all__'
        exclude = ['delete_status', ]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for file_name, field in self.fields.items():
            if file_name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant_id=request.user_obj.pk)
            elif file_name == 'contract_approved':
                continue
            field.widget.attrs.update({'class': 'form-control'})


class CourseRecordForm(forms.ModelForm):

    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for file_name, field in self.fields.items():
            if file_name == 'teacher':
                field.choices = ((request.user_obj.pk,
                                  models.UserInfo.objects.filter(id=request.user_obj.pk).first().username),)
            elif file_name == 'has_homework':
                continue
            field.widget.attrs.update({'class': 'form-control'})


class StudyRecordForm(forms.ModelForm):

    class Meta:
        model = models.StudyRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for file_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
