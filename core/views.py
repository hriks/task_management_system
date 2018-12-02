# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django import views

from core.decorator import auth_required
from core.serializers import TaskSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class Login(views.View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if 'authToken' in request.session:
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


class Dashboard(views.View):
    template_name = "dashboard.html"

    @method_decorator(auth_required())
    def get(self, request, operator, *args, **kwargs):
        return render(request, self.template_name, {
            "operator": operator
        })


class Logout(views.View):

    @method_decorator(auth_required())
    def get(self, request, operator, *args, **kwargs):
        if 'authToken' in request.session:
            request.session.pop('authToken')
        messages.error(
            request, "%s ! You had been logout successfully!" % operator.username.title())  # noqa
        return redirect('/')


@api_view(["GET"])
@auth_required()
def getTasksList(request, operator, *args, **kwargs):
    from core.models import Task
    return Response(TaskSerializer(
        Task.getTasksQueryset(operator), many=True
    ).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@auth_required()
def getNewTasksList(request, operator, *args, **kwargs):
    from core.models import Task
    return Response(TaskSerializer(
        Task.getNewTasksQueryset(operator), many=True
    ).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@auth_required()
def createTask(request, operator, *args, **kwargs):
    try:
        from core.models import Task
        data = request.data
        return Response(TaskSerializer(
            Task.create(
                operator, data['title'], data.get('description', ''),
                data['priority'])
        ).data, status=status.HTTP_201_CREATED)
    except KeyError:
        return Response(
            {"message": "Required fields not found"},
            status=status.HTTP_400_BAD_REQUEST)
    except AssertionError as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        raise e


@api_view(["POST"])
@auth_required()
def updateTask(request, operator, *args, **kwargs):
    try:
        from core.models import Task
        task = Task.objects.get(id=request.data.get("id"))
        task.updateState(operator, **request.data)
        return Response({}, status=status.HTTP_200_OK)
    except KeyError:
        return Response(
            {"message": "Missing required fields"},
            status=status.HTTP_400_BAD_REQUEST)
    except AssertionError as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
