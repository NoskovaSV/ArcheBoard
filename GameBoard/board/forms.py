from django import forms
from django.core.exceptions import ValidationError
from .models import User, Ad
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class AdForm(forms.ModelForm):
   class Meta:
       model = Ad
       fields = [
           'user',
           'categories',
           'title',
           'content',
       ]

   class UserCreationForm(forms.Form):
       error_css_class = 'has-error'
       error_messages = {'password_incorrect':
                             ("Старый пароль не верный. Попробуйте еще раз."),
                         'password_mismatch':
                             ("Пароли не совпадают."),
                         'cod-no':
                             ("Код не совпадает."), }

       def __init__(self, *args, **kwargs):
           super('UserCreationForm', self).__init__(*args, **kwargs)

       code = forms.CharField(required=True, max_length=50, label='Код подтверждения',
                              widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                              error_messages={'required': 'Введите код!',
                                              'max_length': 'Максимальное количество символов 50'})

       def save(self, commit=True):
           profile = super('MyActivationCodeForm', self).save(commit=False)
           profile.code = self.cleaned_data['code']

           if commit:
               profile.save()
           return profile

   class UserCreationForm:
       email = forms.EmailField(required=True, label='Email')
       username = forms.CharField(required=True, max_length=15, label='Логин', min_length=2)
       password1 = forms.CharField(required=True, max_length=30, label='Пароль', min_length=8)
       password2 = forms.CharField(required=True, max_length=30, label='Повторите пароль')
       firstname = forms.CharField(required=True, max_length=25, label='Номер телефона', )

   def clean_username(self):
       username = self.cleaned_data.get("username")
       try:
           User._default_manager.get(username=username)
           raise forms.ValidationError(
               self.error_messages['username_exists'],
               code='username_exists',
           )
       except User.DoesNotExist:
           return username

   def save(self, commit=True):
       user = super('RegistrationForm', self).save(commit=False)
       user.email = self.cleaned_data['email']
       user.first_name = self.cleaned_data['firstname']
       user.password1 = self.cleaned_data['password1']
       user.password2 = self.cleaned_data['password2']
       user.is_active = False

       if commit:
           user.save()
       return user


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user