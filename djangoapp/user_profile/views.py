from typing import Any
from django.shortcuts import render
from django.views import View
from . import models, forms


# Create your views here.


class PerfilBase(View):
    template_name = 'user_profile/pages/create_user.html'

    def setup(self, *args: Any, **kwargs: Any):
        super().setup(*args, **kwargs)
        if self.request.user.is_authenticated:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform': forms.PerfilForm(data=self.request.POST or None),
            }
            self.render = render(
                self.request, self.template_name, self.context
            )

        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                ),
                'perfilform': forms.PerfilForm(data=self.request.POST or None),
            }
            self.render = render(
                self.request, self.template_name, self.context
            )

    def get(self, *args, **kwargs):
        return self.render


class Create(PerfilBase):
    def post(self, *args, **kwargs):
        return self.render


class Upate(View):
    ...


class Login(View):
    ...


class Logout(View):
    ...
