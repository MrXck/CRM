from django import forms


class Login(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        min_length=6,
        widget=forms.widgets.TextInput(attrs={'placeholder': '请输入用户名'}),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '不能小于6位'
        }
    )
    password = forms.CharField(
        label='密码',
        max_length=16,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'placeholder': '请输入密码'}),
        error_messages={
            'required': '密码不能为空',
            'min_length': '不能小于6位'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        min_length=6,
        widget=forms.widgets.TextInput(attrs={'placeholder': '请输入用户名'}),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '不能小于6位'
        }
    )

    password = forms.CharField(
        label='密码',
        max_length=16,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'placeholder': '请输入密码'}),
        error_messages={
            'required': '密码不能为空',
            'min_length': '不能小于6位'
        }
    )

    r_password = forms.CharField(
        label='确认密码',
        max_length=16,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'placeholder': '请再次输入密码'}),
        error_messages={
            'required': '确认密码不能为空',
            'min_length': '不能小于6位'
        }
    )

    telephone = forms.CharField(
        label='手机号',
        max_length=11,
        min_length=11,
        widget=forms.widgets.TextInput(attrs={'placeholder': '请输入手机号'}),
        error_messages={
            'required': '手机号不能为空',
            'min_length': '不能小于11位'
        }
    )

    email = forms.EmailField(
        label='邮箱',
        widget=forms.widgets.EmailInput(attrs={'placeholder': '请输入邮箱'}),
        error_messages={
            'required': '邮箱不能为空',
            'min_length': '不能小于6位'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        value = self.cleaned_data
        if value.get('password') and value.get('r_password'):
            if value.get('password').strip() == value.get('r_password').strip():
                return value
            else:
                self.add_error('r_password', '两次输入的密码不一致')
                raise ValidationError('两次输入的密码不一致')

