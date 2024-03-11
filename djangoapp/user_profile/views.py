from django.views import View
from user_profile.forms import RegisterUserForm, RegisterUpdateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.
class RegisterView(View):
    template_name = 'user_profile/pages/register.html'

    def get(self, request):
        form = RegisterUserForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado com sucesso')

            return redirect('user_profile:login')

        return render(request, self.template_name, {'form': form})


@method_decorator(
    login_required(login_url='user_profile:login'), name='dispatch'
)
class UpdateView(View):
    template_name = 'user_profile/pages/register.html'

    def get(self, request):
        form = RegisterUpdateUserForm(instance=request.user)

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterUpdateUserForm(request.POST, instance=request.user)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        form.save()
        return redirect('user_profile:update')


class LoginView(View):
    template_name = 'user_profile/pages/login.html'

    def get(self, request):
        form = AuthenticationForm(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        print('loguei!!!')
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logado com sucesso')
            return redirect('product_app:index')

        messages.error(request, 'Login invalido')
        return render(request, self.template_name, {'form': form})


@method_decorator(
    login_required(login_url='user_profile:login'), name='dispatch'
)
class LogoutView(View):
    def get(self, request):
        print('desloguei!!!')
        logout(request)
        return redirect('user_profile:login')
