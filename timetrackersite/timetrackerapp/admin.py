from django.contrib import admin
from .models import Pracownik, CzasPracy, Przerwa
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import string, random


class MyUserChangeForm(UserChangeForm):
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]


class MyUserCreationForm(UserCreationForm):

    #todo add email field!

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        p = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        print(p)
        self.fields['password1'].widget.attrs.update({'value': p})
        self.fields['password2'].widget.attrs.update({'value': p})

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        #todo sending email!
        return user


# Define a new User admin
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm


# Register your models here.
admin.site.register(Pracownik)  # 1
admin.site.register(CzasPracy)  # 2
admin.site.register(Przerwa)  # 3

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
