from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login



class MainPage(LoginRequiredMixin, TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


def login_page(request, next_page):
    context = {"declined": False}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(form.cleaned_data['next_page'])
            else:
                context['declined'] = True
    else:
        form = LoginForm()
        form.next_page = next_page
