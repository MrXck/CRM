import re

from django import template
from django.urls import reverse
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def reverse_url(request):
    if request.path == reverse('customers'):
        return '公户信息'
    elif request.path == reverse('my_customers'):
        return '我的客户信息'
    elif request.path == reverse('consult_record'):
        return '我的跟进记录'


@register.simple_tag
def next_url(request, url, customer_id):
    q = QueryDict(mutable=True)
    q['next'] = request.get_full_path()
    full_path = q.urlencode()
    return reverse(url, args=(customer_id,)) + '?' + full_path


@register.inclusion_tag('menu.html')
def menu(request):
    for v in request.left_tab.values():
        if re.match(v['permissions__url'], request.path):
            v['class'] = 'active'
        for i in v['children']:
            if re.match(i['permissions__url'], request.path):
                v['class'] = 'active'

    return {'menu_list': request.left_tab}


@register.filter
def panduan(request, url_name):
    for i in request.qu_list:
        if i == url_name:
            return True
    return False


@register.inclusion_tag('bread.html')
def bread(request):
    di = []
    for v in request.left_tab.values():
        if re.match(v['permissions__url'], request.path):
            v['class'] = 'active'
            di.append(v)
        for i in v['children']:
            if re.match(i['permissions__url'], request.path):
                i['class'] = 'active'
                di.append(v)
                di.append(i)
    return {'dict': di}


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()


def digui(left_tab, di, request):
    for i in left_tab:
        if re.match(i['permissions__url'], request.path):
            i['class'] = 'active'
            di.append(i)
