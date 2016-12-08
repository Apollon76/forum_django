from django import forms
from django.utils.safestring import mark_safe


class RegistrationForm(forms.Form):
    '''
    def __init__(self, *args, **kwargs):

        self.captcha_id = kwargs.pop('captcha_id')
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['captcha'] = forms.CharField(label=mark_safe('<img src={}>'.format(self.captcha_data[self.captcha_id][0])),
                                                 max_length=10)
        self.fields['captcha_id'] = forms.HiddenInput(value=str(self.captcha_id))
    '''
    captcha_data = (('/static/captcha1.jpg', '8anf'),
                    ('/static/captcha2.jpg', ''))
    nickname = forms.CharField(label='Nickname', max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput())
    email = forms.EmailField(label='E-mail', max_length=30)
    #captcha = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput())


class PostForm(forms.Form):
    data = forms.CharField(label='Message', widget=forms.Textarea)


class NewThreadForm(forms.Form):
    name = forms.CharField(label='Thread name', max_length=30)

