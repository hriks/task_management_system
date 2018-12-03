# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from core.models import Task, Operator
from core.forms import OperatorForm


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    form = OperatorForm
    list_display = ("username", "operator_type", "created")
    search_fields = ('username',)
    list_filter = ('operator_type',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "accepted_by", "priority", "state")
    search_fields = ("accepted_by__username", "created_by__username")
    list_filter = ("state", "priority")
    raw_id_fields = ("accepted_by", "created_by")
