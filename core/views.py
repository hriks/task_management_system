# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django import views

from django.contrib import messages
from django.utils.decorators import method_decorator


class Login(views.View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if 'access_token' in request.session:
            return redirect('/home')
        return render(request, self.template_name)

    @method_decorator(views.decorators.csrf.csrf_exempt)
    def post(self, request, *args, **kwargs):
        from core.models import Operator
        authToken, message = Operator.validateOperator(request)
        messages.error(request, message)
        if authToken:
            request.session['authToken'] = authToken
            return redirect('/home')
        return redirect('/')
