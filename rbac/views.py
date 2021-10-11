from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from rbac import models
from django.db.models import Q
from app01.models import UserInfo

# Create your views here.


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'
        exclude = ['permissions', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class PermissionModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


def role_list(request):
    role_obj = models.Role.objects.all()
    return render(request, 'role_list.html', {'objs': role_obj})


def role_add(request):
    if request.method == 'GET':
        role_model_form = RoleModelForm()
        return render(request, 'form.html', {'form_obj': role_model_form})
    else:
        role_model_form = RoleModelForm(request.POST)
        if role_model_form.is_valid():
            role_model_form.save()
            return redirect('role_list')
        else:
            return render(request, 'form.html', {'form_obj': role_model_form})


def role_edit(request, cid):
    role_obj = models.Role.objects.filter(pk=cid).first()
    if request.method == 'GET':
        role_model_form = RoleModelForm(instance=role_obj)
        return render(request, 'form.html', {'form_obj': role_model_form})
    else:
        role_model_form = RoleModelForm(request.POST, instance=role_obj)
        if role_model_form.is_valid():
            role_model_form.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'form.html', {'form_obj': role_model_form})


def role_del(request, cid):
    models.Role.objects.filter(pk=cid).first().delete()
    return redirect(request.GET.get('next'))


def menu_list(request):
    menu_objs = models.Menu.objects.all()
    mid = request.GET.get('mid')
    d1 = {}
    objs = models.Permission.objects.filter(Q(menus_id=mid) | Q(parent__menus_id=mid)).values(
            'id',
            'menus_id',
            'parent_id',
            'url_name',
            'url',
            'title',
            'id',
            'menus__title',
            'parent__title',
        )
    for i in objs:
        if not i['parent_id']:
            d1[i['id']] = i
            d1[i['id']]['children'] = []
    for i in objs:
        if i['parent_id']:
            d1[i['parent_id']]['children'].append(i)
    return render(request, 'menu_list.html', {'objs': menu_objs, 'permission_objs': d1.values()})


def menu_add(request):
    if request.method == 'GET':
        menu_model_form = MenuModelForm()
        return render(request, 'form.html', {'form_obj': menu_model_form})
    else:
        menu_model_form = MenuModelForm(request.POST)
        if menu_model_form.is_valid():
            menu_model_form.save()
            return redirect('menu_list')
        else:
            return render(request, 'form.html', {'form_obj': menu_model_form})


def menu_edit(request, cid):
    menu_obj = models.Menu.objects.filter(pk=cid).first()
    if request.method == 'GET':
        menu_model_form = MenuModelForm(instance=menu_obj)
        return render(request, 'form.html', {'form_obj': menu_model_form})
    else:
        menu_model_form = MenuModelForm(request.POST, instance=menu_obj)
        if menu_model_form.is_valid():
            menu_model_form.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'form.html', {'form_obj': menu_model_form})


def menu_del(request, cid):
    models.Menu.objects.filter(pk=cid).delete()
    return redirect(request.GET.get('next'))


def permission_add(request):
    if request.method == 'GET':
        permission_model_form = PermissionModelForm()
        return render(request, 'form.html', {'form_obj': permission_model_form})
    else:
        permission_model_form = PermissionModelForm(request.POST)
        if permission_model_form.is_valid():
            permission_model_form.save()
            return redirect('menu_list')
        else:
            return render(request, 'form.html', {'form_obj': permission_model_form})


def permission_edit(request, cid):
    permission_obj = models.Permission.objects.filter(pk=cid).first()
    if request.method == 'GET':
        permission_model_form = PermissionModelForm(instance=permission_obj)
        return render(request, 'form.html', {'form_obj': permission_model_form})
    else:
        permission_model_form = PermissionModelForm(request.POST, instance=permission_obj)
        if permission_model_form.is_valid():
            permission_model_form.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'form.html', {'form_obj': permission_model_form})


def permission_del(request, cid):
    models.Permission.objects.filter(pk=cid).delete()
    return redirect(request.GET.get('next'))


def distribute_permissions(request):
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user_obj = UserInfo.objects.filter(id=uid).first()
        if not user_obj:
            return HttpResponse('用户不存在')
        user_obj.roles.set(request.POST.getlist('roles'))
    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role_obj = models.Role.objects.filter(id=rid).first()
        if not role_obj:
            return HttpResponse('用户不存在')
        role_obj.permissions.set(request.POST.getlist('permissions'))
    user_objs = UserInfo.objects.all()
    user_has_roles = UserInfo.objects.filter(id=uid).values('id', 'roles')
    user_has_roles_dict = {item['roles']: None for item in user_has_roles}
    role_objs = models.Role.objects.all()

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id', 'permissions')
    elif uid and not rid:
        user = UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('此用户不存在')
        role_has_permissions = user.roles.values('id', 'permissions')
    else:
        role_has_permissions = []
    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}
    all_menu_list = []

    queryset = models.Menu.objects.values('id', 'title')
    menu_dict = {}

    for item in queryset:
        item['children'] = []
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    root_permission = models.Permission.objects.filter(menus__isnull=False).values('id', 'title', 'menus_id')
    root_permission_dict = {}

    for per in root_permission:
        per['children'] = []
        nid = per['id']
        menu_id = per['menus_id']
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(menus__isnull=True).values('id', 'title', 'parent_id')

    for per in node_permission:
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(request, 'distribute_permissions.html', {
        'user_list': user_objs,
        'role_list': role_objs,
        'user_has_roles_dict': user_has_roles_dict,
        'role_has_permissions_dict': role_has_permissions_dict,
        'all_menu_list': all_menu_list,
        'uid': uid,
        'rid': rid,
    })
