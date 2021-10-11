import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from app01 import models


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path in [reverse('login'), reverse('register'), reverse('log_out')]:
            return
        # elif 'admin' in request.path:
        #     return
        elif request.session.get('user_id'):
            user_obj = models.UserInfo.objects.get(id=request.session.get('user_id'))
            request.user_obj = user_obj
            user_ = user_obj
            permission_list = user_.roles.values(
                'permissions__parent_id',
                'permissions__title',
                'permissions__id',
                'permissions__url',
                'permissions__url_name',
                'permissions__menus_id',
                'permissions__menus__title',
                'permissions__menus__weight',
            ).order_by('-permissions__menus__weight').distinct()
            di = {}
            quanxian = []
            qu_list = []
            for i in permission_list:
                qu_list.append(i['permissions__url_name'])
                quanxian.append(i['permissions__url'])
                if not i['permissions__parent_id']:
                    di[i['permissions__id']] = i
                    di[i['permissions__id']]['children'] = []
            for i in permission_list:
                if i['permissions__parent_id']:
                    di[i['permissions__parent_id']]['children'].append(i)
            request.left_tab = di
            request.quanxian = quanxian
            request.qu_list = qu_list
            for i in request.quanxian:
                if re.match(i, request.path):
                    return
        return redirect('login')
