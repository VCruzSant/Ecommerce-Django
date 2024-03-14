from django.views import View
from user_profile.forms import (
    RegisterUserForm, RegisterUpdateUserForm, ProfileForm
)
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from user_profile.models import UserProfile
import copy


# Create your views here.
class RegisterView(View):
    template_name = 'user_profile/pages/register.html'

    def get(self, request):
        form_user = RegisterUserForm()
        form_profile = ProfileForm()

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

            password = form_user.cleaned_data.get('password')

            if password:
                athentic = authenticate(
                    self.request, username=user, password=password
                )

                if athentic:
                    login(self.request, user=user)

            messages.success(request, 'Usuário registrado com sucesso')
            return redirect('user_profile:login')

        return render(request, self.template_name,
                      {
                          'form_user': form_user,
                          'form_profile': form_profile,
                      }
                      )


@method_decorator(
    login_required(login_url='user_profile:login'), name='dispatch',
)
class UpdateView(View):
    template_name = 'user_profile/pages/register.html'

    def get(self, request):
        profile = UserProfile.objects.filter(
            user=request.user
        ).first()
        form_user = RegisterUpdateUserForm(instance=request.user)
        form_profile = ProfileForm(instance=profile)

        return render(request, self.template_name,
                      {
                          'form_user': form_user,
                          'form_profile': form_profile,
                      }
                      )

    @method_decorator(csrf_protect)
    def post(self, request):
        cart = copy.deepcopy(request.session.get('cart', {}))
        form_user = RegisterUpdateUserForm(request.POST)
        form_profile = ProfileForm(request.POST)

        if form_user.is_valid() and form_profile.is_valid():
            print('o form é valido')
            user = form_user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()

            request.session['cart'] = cart
            request.session.save()

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
