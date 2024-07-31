from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'middle_name', 'birthday', 'phone', 'password1', 'password2')

        def clean_birthday(self):
            birthday = self.cleaned_data.get('birthday')
            if not birthday:
                raise forms.ValidationError('Дата рождения обязательна для заполнения.')
            return birthday


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'middle_name', 'email', 'phone', 'birthday')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
