# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

import uuid
import json


class Vault(models.Model):
    operator_id = models.CharField(max_length=128)
    password = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        try:
            current = Vault.objects.get(id=self.id)
            if (current.password != str(self.password)):
                self.password = Vault.get_hashed_password(str(self.password))
        except Vault.DoesNotExist:
            self.password = Vault.get_hashed_password(str(self.password))
        super(Vault, self).save(*args, **kwargs)

    @staticmethod
    def get_hashed_password(password):
        # Hash a password for the first time
        # Using bcrypt, the salt is saved into the hash itself
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    def check_password(self, password):
        """
        check hased password. Using bcrypt, the salt is saved into the
        hash itself
        """
        import bcrypt
        try:
            return bcrypt.hashpw(
                str(password), str(self.password)) == str(self.password)
        except Exception:
            # If Password has invalid Salt
            return False


class Operator(models.Model):
    """
    Stores the basic information about operator
    """
    TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('delivery_person', 'Delivery Person')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=6, unique=True)
    operator_type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default='delivery_person')
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, *args, **kwargs):
        instance, created = cls.objects.get_or_create(
            username=kwargs.get('username', ''))
        if created:
            Vault.objects.create(
                operator_id=instance.id,
                password=kwargs.get('password', ''))
        instance.operator_type = kwargs.get('operator_type')
        instance.save()
        return instance

    @property
    def vault(self, model='vault'):
        return ContentType.objects.get(
            app_label='core', model=model
        ).model_class().objects.get(operator_id=self.id)

    @classmethod
    def getAuthenticatedOperator(cls, request):
        """ Decorator uses this method to get authenticated user
        """
        try:
            data = json.loads(request.session['authToken'])
            return cls.objects.get(username=data['username'])
        except cls.DoesNotExist:
            return None

    def accessToken(self):
        """ Generate the accessToken, currently using simple JSON.
        JWT Token or any other strong algo can be used to generate
        this accessToken
        """
        return json.dumps({"username": self.username})

    @classmethod
    def validateOperator(cls, request):
        """ This class method validate users form when he tries to login
        return accessToken will be saved in session.
        """
        data = request.POST.dict()
        try:
            operator = cls.objects.get(
                username=data.get('username', '').lower())
            validated = operator.vault.check_password(
                data.get('password', ''))
            if validated:
                return operator.accessToken(), "Hi %s!. You had been successfully authenticated." % operator.username  # noqa
            return None, "Invalid Password Provided."
        except cls.DoesNotExist:
            return None, 'Invalid Username Provided.'
        return None, 'Something went wrong! Please try again.'


class Task(models.Model):
    PRIORITY_CHOICES = (('low', 'Low'), ('medium', 'Medium'), ('high', 'High'))
    STATE_CHOICES = (
        ('new', 'New'), ('cancelled', 'Cancelled'),
        ('accepted', 'Accepted'), ('declined', 'Declined'),
        ('completed', 'Completed')
    )
    title = models.CharField(max_length=128)
    description = models.TextField()
    created_by = models.ForeignKey(Operator, related_name='creator')
    accepted_by = models.ForeignKey(
        Operator, related_name='delivery_person', null=True, blank=True)
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES)
    state = models.CharField(
        max_length=16, choices=STATE_CHOICES, default='new')
    timeline = JSONField(default=[])
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            current = Task.objects.get(id=self.id)
            if current.state != self.state or current.accepted_by != self.accepted_by:  # noqa
                self.addTimeline()
        except Task.DoesNotExist:
            self.addTimeline()
        super(Task, self).save(*args, **kwargs)

    def addTimeline(self):
        self.timeline.append({
            "state": self.state,
            "time": timezone.now().strftime("%d/%m/%Y %H:%M:%S"),
            "created_by": self.created_by.username,
            "accepted_by": self.accepted_by.username if self.accepted_by else '-'  # noqa
        })

    def updateState(self, operator=None, **data):
        self.state = data.get('state')
        if self.state == 'accepted' and operator:
            assert Task.objects.filter(
                state="accepted", accepted_by=operator
            ).count() < 3, "Delivery Person could not have more than 3 pending tasks."  # noqa
            self.accepted_by = operator
        if self.state == 'declined' and self.accepted_by:
            self.state = 'new'
            self.accepted_by = None
        self.save()

    @classmethod
    def create(cls, operator, title, description, priority="low"):
        assert operator.operator_type == 'manager', 'Only manager can create new ticket.'  # noqa
        return cls.objects.create(
            title=title, created_by=operator, description=description,
            priority=priority)

    @classmethod
    def getTasksQueryset(cls, operator=None):
        queryset = cls.objects.exclude(state__in=['new', 'cancelled'])
        if operator and operator.operator_type == 'delivery_person':
            queryset = queryset.filter(accepted_by=operator)
        return queryset

    @classmethod
    def getNewTasksQueryset(cls, operator=None):
        queryset = cls.objects.filter(state="new")
        if operator and operator.operator_type == 'delivery_person':
            queryset = queryset.objects.filter(
                operator=operator, priority="high").earliest('created')
        return queryset
