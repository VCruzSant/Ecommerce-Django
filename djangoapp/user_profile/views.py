from django.views import View
from user_profile.forms import (
    RegisterUserForm, RegisterUpdateUserForm, ProfileForm
)
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.contrib import messages
import copy


# Create your views here.
class RegisterView(View):
    template_name = 'user_profile/pages/register.html'

    def get(self, request):
        form_user = RegisterUserForm(instance=request.user)
        form_profile = ProfileForm(instance=request.user)

        return render(request, self.template_name,
                      {
                          'form_user': form_user,
                          'form_profile': form_profile,
                      }
                      )

    def post(self, request):
        form_user = RegisterUserForm(request.POST)
        form_profile = ProfileForm(request.POST)

        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save()  # Salva o objeto User e obtém a instância
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Usuário registrado com sucesso')
            return redirect('user_profile:login')

        return render(request, self.template_name,
                      {
                          'form_user': form_user,
                          'form_profile': form_profile,
                      }
                      )


@method_decorator(
    login_required(login_url='user_profile:login'), name='dispatch'
)
class UpdateView(View):
    template_name = 'user_profile/pages/register.html'

    def get(self, request):
        self.cart = copy.deepcopy(self.request.session.get('cart', {}))
        form_user = RegisterUpdateUserForm(instance=request.user)
        form_profile = ProfileForm(instance=request.user)

        return render(request, self.template_name,
                      {
                          'form_user': form_user,
                          'form_profile': form_profile,
                      }
                      )

    def post(self, request):
        form_user = RegisterUserForm(request.POST)
        form_profile = ProfileForm(request.POST)

        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()

            self.request.session['cart'] = self.cart
            self.request.session.save()

            messages.success(request, 'Usuário registrado com sucesso')
            return redirect('user_profile:login')

        return render(request, self.template_name,
                      {
                          'form_user': form_user,
                          'form_profile': form_profile,
                      }
                      )


class LoginView(View):
    template_name = 'user_profile/pages/login.html'

    def get(self, request):
        form_user = AuthenticationForm(request)
        return render(request, self.template_name, {'form_user': form_user})

    def post(self, request):
        print('loguei!!!')
        form_user = AuthenticationForm(request, data=request.POST)

        if form_user.is_valid():
            user = form_user.get_user()
            login(request, user)
            messages.success(request, 'Logado com sucesso')
            return redirect('product_app:index')

        messages.error(request, 'Login invalido')
        return render(request, self.template_name, {'form_user': form_user})


@method_decorator(
    login_required(login_url='user_profile:login'), name='dispatch'
)
class LogoutView(View):
    def get(self, request):
        print('desloguei!!!')
        logout(request)
        return redirect('user_profile:login')
