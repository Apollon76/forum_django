from django import forms


class RegistrationForm(forms.Form):
    nickname = forms.CharField(label='Nickname', max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput())
    email = forms.EmailField(label='E-mail', max_length=30)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput())


class PostForm(forms.Form):
    data = forms.CharField(label='Message')


class NewThreadForm(forms.Form):
    name = forms.CharField(label='Thread name', max_length=30)

