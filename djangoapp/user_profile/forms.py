from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = 'user',


class UserForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
    )

    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Password Confirm'
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'password', 'password_confirm', 'email',
        )

    # fields validation
    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_messages = {}

        # o que o usuário está enviando
        user_data = cleaned.get('username')
        email = cleaned.get('email')
        password = cleaned.get('password')
        password_confirm = cleaned.get('password_confirm')

        # o que já está no banco de dados
        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email).first()

        error_msg_user_exists = 'User already exists'
        error_msg_user_email = 'E-mail already exists'
        error_msg_password = "Passwords don't match"

        if self.user:
            if user_data != user_db:
                if user_db:
                    validation_error_messages['username'] = (
                        error_msg_user_exists
                    )

            if email != email_db:
                if email_db:
                    validation_error_messages['email'] = (
                        error_msg_user_email
                    )

            if password:
                if password != password_confirm:
                    validation_error_messages['password_confirm'] = (
                        error_msg_password
                    )

        if validation_error_messages:
            raise (forms.ValidationError(validation_error_messages))
