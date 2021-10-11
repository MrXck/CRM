import hashlib
import re

from django.forms.fields import DateField
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe

from app01 import models
from app01.form import Login, RegisterForm
from app01.modelform import CustomerForm, ConsultRecordForm, EnrollmentForm, CourseRecordForm, StudyRecordForm


def login(request):
    if request.method == 'GET':
        user_obj = Login()
        return render(request, 'login.html', {'user_obj': user_obj})
    else:
        form_data = request.POST
        user_obj = Login(form_data)
        if user_obj.is_valid():
            password = set_md5(request.POST.get('password').strip())
            user = models.UserInfo.objects.filter(username=request.POST.get('username').strip(),
                                                  password=password).first()
            if user:
                request.session['user_id'] = user.id
                return redirect('customers')
            else:
                user_obj.add_error('password', '用户名或密码错误')
                return render(request, 'login.html', {'user_obj': user_obj})
        else:
            return render(request, 'login.html', {'user_obj': user_obj})


def register(request):
    if request.method == 'GET':
        register_obj = RegisterForm()
        return render(request, 'register.html', {'register_obj': register_obj})
    else:
        register_obj = RegisterForm(request.POST)
        if register_obj.is_valid():
            user_obj = models.UserInfo.objects.filter(username=request.POST.get('username').strip())
            if not user_obj:
                register_obj.cleaned_data.pop('r_password')
                register_obj.cleaned_data['password'] = set_md5(register_obj.cleaned_data.get('password').strip())
                models.UserInfo.objects.create(**register_obj.cleaned_data)
                return redirect('login')
            else:
                register_obj.add_error('username', '用户名已存在')
                return render(request, 'register.html', {'register_obj': register_obj})
        else:
            return render(request, 'register.html', {'register_obj': register_obj})


def home(request):
    return render(request, 'home.html')


def customers(request):
    if request.method == 'GET':
        query = {}
        return get_data(request, query, 'home.html')
    else:
        action = request.POST.get('action')
        cids = request.POST.getlist('cids[]')
        if action == 'to_si':
            customer_obj = models.Customer.objects.filter(pk__in=cids, consultant__isnull=True)
            if customer_obj.count() != len(cids):
                return JsonResponse({'code': 1})
            customer_obj.update(consultant_id=request.user_obj.pk)
        else:
            customer_obj = models.Customer.objects.filter(pk__in=cids, consultant_id=request.user_obj.pk)
            customer_obj.update(consultant=None)
        return JsonResponse({'code': 0})


def add_customer(request):
    if request.method == 'GET':
        customer_form_obj = CustomerForm()
        return render(request, 'add_edit_customer.html', {'customer_form_obj': customer_form_obj})
    else:
        customer_form_obj = CustomerForm(request.POST)
        if customer_form_obj.is_valid():
            customer_form_obj.save()
            return redirect('customers')
        else:
            return render(request, 'add_edit_customer.html', {'customer_form_obj': customer_form_obj})


def edit_customer(request, customer_id):
    customer_obj = models.Customer.objects.filter(pk=customer_id).first()
    if request.method == 'GET':
        customer_form_obj = CustomerForm(instance=customer_obj)
        return render(request, 'add_edit_customer.html', {'customer_form_obj': customer_form_obj})
    else:
        customer_form_obj = CustomerForm(request.POST, instance=customer_obj)
        if customer_form_obj.is_valid():
            customer_form_obj.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'add_edit_customer.html', {'customer_form_obj': customer_form_obj})


# def delete_customer(request, customer_id):
#     models.Customer.objects.filter(pk=customer_id).first().delete()
#     return redirect('customers')


def consult_record(request):
    if request.method == 'GET':
        query = {'delete_status': False}
        return get_data(request, query, 'consult_record.html')
    else:
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        if action == 'bulk_delete':
            models.ConsultRecord.objects.filter(pk__in=cids).update(delete_status=True)
        return redirect('consult_record')


def edit_consult_record(request, customer_id):
    consult_record_obj = models.ConsultRecord.objects.filter(id=customer_id).first()
    if request.method == 'GET':
        consult_record_form_obj = ConsultRecordForm(request, instance=consult_record_obj)
        return render(request, 'add_edit_consult_record.html', {'consult_record_form_obj': consult_record_form_obj})
    else:
        consult_record_form_obj = ConsultRecordForm(request, request.POST, instance=consult_record_obj)
        if consult_record_form_obj.is_valid():
            consult_record_form_obj.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'add_edit_consult_record.html', {'consult_record_form_obj': consult_record_form_obj})


def add_consult_record(request):
    if request.method == 'GET':
        consult_record_form_obj = ConsultRecordForm(request)
        return render(request, 'add_edit_consult_record.html', {'consult_record_form_obj': consult_record_form_obj})
    else:
        consult_record_form_obj = ConsultRecordForm(request, request.POST)
        if consult_record_form_obj.is_valid():
            consult_record_form_obj.save()
            return redirect('consult_record')
        else:
            return render(request, 'add_edit_consult_record.html', {'consult_record_form_obj': consult_record_form_obj})


def delete_consult_record(request, consult_record_id):
    models.ConsultRecord.objects.filter(pk=consult_record_id).update(delete_status=True)
    return redirect(request.GET.get('next'))


def enrollment(request):
    if request.method == 'GET':
        query = {'delete_status': False}
        return get_data(request, query, 'enrollment.html')
    else:
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        if action == 'bulk_delete':
            models.Enrollment.objects.filter(pk__in=cids).update(delete_status=True)
        return redirect('enrollment')


def add_enrollment(request):
    if request.method == 'GET':
        enrollment_form_obj = EnrollmentForm(request)
        return render(request, 'add_edit_enrollment.html', {'enrollment_form_obj': enrollment_form_obj})
    else:
        enrollment_form_obj = EnrollmentForm(request, request.POST)
        if enrollment_form_obj.is_valid():
            enrollment_form_obj.save()
            return redirect('enrollment')
        else:
            return render(request, 'add_edit_enrollment.html', {'enrollment_form_obj': enrollment_form_obj})


def edit_enrollment(request, customer_id):
    enrollment_obj = models.Enrollment.objects.filter(id=customer_id).first()
    if request.method == 'GET':
        enrollment_form_obj = EnrollmentForm(request, instance=enrollment_obj)
        return render(request, 'add_edit_enrollment.html', {'enrollment_form_obj': enrollment_form_obj})
    else:
        enrollment_form_obj = ConsultRecordForm(request, request.POST, instance=enrollment_obj)
        if enrollment_form_obj.is_valid():
            enrollment_form_obj.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'add_edit_enrollment.html', {'enrollment_form_obj': enrollment_form_obj})


def delete_enrollment(request, enrollment_id):
    models.Enrollment.objects.filter(pk=enrollment_id).update(delete_status=True)
    return redirect(request.GET.get('next'))


def course_record(request):
    if request.method == 'GET':
        query = {}
        return get_data(request, query, 'course_record.html')
    else:
        action = request.POST.get('action')
        cids = request.POST.getlist('cids[]')
        if action == 'bulk_create_srecord':
            for cid in cids:
                course_record_obj = models.CourseRecord.objects.filter(pk=cid).first()
                students = course_record_obj.re_class.customer_set.filter(status='studying')
                obj_list = []
                for student in students:
                    obj = models.StudyRecord(course_record=course_record_obj, student=student)
                    obj_list.append(obj)
                try:
                    models.StudyRecord.objects.bulk_create(obj_list)
                except:
                    return JsonResponse({'code': 2})
        # elif action == 'bulk_delete':
        #     models.CourseRecord.objects.filter(pk__in=cids).delete()
        return JsonResponse({'code': 0})


def add_course_record(request):
    if request.method == 'GET':
        course_record_form_obj = CourseRecordForm(request)
        return render(request, 'add_edit_course_record.html', {'course_record_form_obj': course_record_form_obj})
    else:
        course_record_form_obj = CourseRecordForm(request, request.POST)
        if course_record_form_obj.is_valid():
            course_record_form_obj.save()
            return redirect('course_record')
        else:
            return render(request, 'add_edit_course_record.html', {'course_record_form_obj': course_record_form_obj})


def edit_course_record(request, customer_id):
    course_record_obj = models.CourseRecord.objects.filter(id=customer_id).first()
    if request.method == 'GET':
        course_record_form_obj = CourseRecordForm(request, instance=course_record_obj)
        return render(request, 'add_edit_course_record.html', {'course_record_form_obj': course_record_form_obj})
    else:
        course_record_form_obj = CourseRecordForm(request, request.POST, instance=course_record_obj)
        if course_record_form_obj.is_valid():
            course_record_form_obj.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'add_edit_course_record.html', {'course_record_form_obj': course_record_form_obj})


def study_record(request, course_record_id):
    query = {'course_record_id': course_record_id}
    if request.method == 'GET':
        return get_data(request, query, 'study_record.html')
    else:
        customer_all_objs = modelformset_factory(models.StudyRecord, StudyRecordForm, extra=0)
        customer_all_objs = customer_all_objs(request.POST)
        if customer_all_objs.is_valid():
            customer_all_objs.save()
            return redirect(reverse('study_record', args=(course_record_id, )))
        else:
            return get_data(request, query, 'study_record.html')


def add_study_record(request):
    if request.method == 'GET':
        study_record_form_obj = StudyRecordForm(request)
        return render(request, 'add_edit_study_record.html', {'study_record_form_obj': study_record_form_obj})
    else:
        study_record_form_obj = StudyRecordForm(request, request.POST)
        if study_record_form_obj.is_valid():
            study_record_form_obj.save()
            return redirect('study_record')
        else:
            return render(request, 'add_edit_study_record.html', {'study_record_form_obj': study_record_form_obj})


def edit_study_record(request, customer_id):
    study_record_obj = models.StudyRecord.objects.filter(id=customer_id).first()
    if request.method == 'GET':
        study_record_form_obj = StudyRecordForm(request, instance=study_record_obj)
        return render(request, 'add_edit_study_record.html', {'study_record_form_obj': study_record_form_obj})
    else:
        study_record_form_obj = StudyRecordForm(request, request.POST, instance=study_record_obj)
        if study_record_form_obj.is_valid():
            study_record_form_obj.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'add_edit_study_record.html', {'study_record_form_obj': study_record_form_obj})


def log_out(request):
    request.session.flush()
    return redirect('login')


# 以下函数与用户访问无关
def fen_page(show_page_num, page, objs, url):
    page_previous = page - 1
    page_next = page + 1
    half_page_num = show_page_num // 2
    if objs >= show_page_num:
        if page + half_page_num > objs:
            start_page = objs - show_page_num + 1
            end_page = start_page + show_page_num
        elif page <= half_page_num:
            start_page = 1
            end_page = show_page_num + start_page
        else:
            start_page = page - half_page_num
            end_page = start_page + show_page_num
    else:
        start_page = 1
        end_page = objs + 1
    page_list = range(start_page, end_page)
    html = page_html(page_previous, page_next, page_list, page, url, objs)
    return html


def page_html(page_previous, page_next, page_list, page, url, objs):
    first_page = f'<li><a href="{url}1" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'
    last_page = f'<li><a href="{url}{objs}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>'
    if page_previous > 0:
        page_previous = f'<li><a href="{url}{page_previous}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
    else:
        first_page = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'
        page_previous = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
    if page_next <= page_list[-1]:
        page_next = f'<li><a href="{url}{page_next}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
    else:
        last_page = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>'
        page_next = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
    html = f'<nav aria-label="Page navigation"><ul class="pagination">{first_page}{page_previous}'
    for i in page_list:
        if i == page:
            html += f'<li class="active"><a href="{url}{i}">{i}</a></li>'
        else:
            html += f'<li><a href="{url}{i}">{i}</a></li>'
    html += page_next
    html += last_page
    return mark_safe(html)


def get_customers_data(request, page_url, query):
    page = 1
    if request.GET.get('page'):
        try:
            if int(request.GET.get('page').strip()) > 0:
                page = int(request.GET.get('page').strip())
            else:
                return redirect(page_url + '1')
        except ValueError:
            return redirect(page_url + '1')
    if request.path == reverse('customers'):
        customer_all_objs = models.Customer.objects.filter(**query, consultant__isnull=True)
    elif request.path == reverse('consult_record'):
        customer_id = request.GET.get('cid')
        if customer_id:
            query = {'delete_status': False, 'customer_id': customer_id}
        customer_all_objs = models.ConsultRecord.objects.filter(**query, consultant_id=request.user_obj.pk).order_by('-date')
    elif request.path == reverse('enrollment'):
        customer_id = request.GET.get('cid')
        if customer_id:
            query = {'delete_status': False, 'customer_id': customer_id}
        customer_all_objs = models.Enrollment.objects.filter(**query, customer__consultant_id=request.user_obj.pk).order_by('-enrolled_date')
    elif request.path == reverse('course_record'):
        customer_all_objs = models.CourseRecord.objects.filter(**query, teacher_id=request.user_obj.pk).order_by('-date')
    elif '/study_record/' in request.path:
        customer_all_objs = modelformset_factory(models.StudyRecord, StudyRecordForm, extra=0)
        customer_all_objs = customer_all_objs(queryset=models.StudyRecord.objects.filter(**query))
    else:
        customer_all_objs = models.Customer.objects.filter(**query, consultant_id=request.user_obj.pk)
    show_data_num = 10
    show_page_num = 5
    if len(customer_all_objs) > 0:
        customer_objs = customer_all_objs[(page - 1) * show_data_num:page * show_data_num]
        objs = divmod(len(customer_all_objs), show_data_num)
        if objs[1] > 0:
            objs_num = objs[0] + 1
        else:
            objs_num = objs[0]
        if (page - 1) * show_data_num >= len(customer_all_objs):
            return redirect(f'{page_url}' + str(objs_num))
        html = fen_page(show_page_num, page, objs_num, page_url)
    else:
        customer_objs = False
        html = False
    if '/study_record/' in request.path:
        return (customer_objs, customer_all_objs), html
    else:
        return customer_objs, html


def get_data(request, query, html_name):
    search_type = request.GET.get('type')
    key_word = request.GET.get('kw')
    if search_type and key_word:
        query = {search_type.strip() + '__contains': key_word.strip()}
        try:
            objs, html = get_customers_data(request, request.path + '?' + re.sub('&page=\d+', '', request.GET.urlencode()) + '&page=', query)
        except ValueError:
            return get_customers_data(request,  request.path + '?' + re.sub('&page=\d+', '', request.GET.urlencode()) + '&page=', query)
        if '/study_record/' in request.path:
            return render(request, html_name, {'objs': objs[0], 'page_html': html, 'kw': key_word, 'search_type': search_type, 'formset': objs[1]})
        return render(request, html_name, {'objs': objs, 'page_html': html, 'kw': key_word, 'search_type': search_type})
    try:
        objs, html = get_customers_data(request, request.path + '?page=', query)
    except ValueError:
        return get_customers_data(request, request.path + '?' + re.sub('page=\d+', '', request.GET.urlencode()) + '?page=', query)
    if '/study_record/' in request.path:
        return render(request, html_name, {'objs': objs[0], 'page_html': html, 'formset': objs[1]})
    return render(request, html_name, {'objs': objs, 'page_html': html})


def set_md5(value):
    md5_value = hashlib.md5(b'xckdashuaibi')
    md5_value.update(value.encode('utf-8'))
    return md5_value.hexdigest()
