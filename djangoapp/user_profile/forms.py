from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from user_profile.models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'  # type: ignore
        exclude = ('user',)


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=4
    )
    last_name = forms.CharField(
        required=True,
        min_length=4
    )
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        print(f'ESSE É O CEP {self.cleaned_data.get('cep')}')

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'Já existe usuários com esse e-mail', code='invalid'
                    )
                )
            return email

    def clean_user(self):
        user = self.cleaned_data.get('username')

        if User.objects.filter(username=user).exists():
            self.add_error(
                'username',
                ValidationError(
                    'Já existe usuários com esse username', code='invalid'
                )
            )
            return user


class RegisterUpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username'
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não são iguais')
                )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        print(self.instance)

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'Já existe usuários com esse e-mail', code='invalid'
                    )
                )
            return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as e:
                self.add_error(
                    'password1',
                    ValidationError(e)
                )

        return password1
