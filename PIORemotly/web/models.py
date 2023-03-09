from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    name = models.TextField()
    members = models.ManyToManyField(User, through="UserMembership")

    def __str__(self):
        return self.name


class UserMembership(models.Model):
    class UserRole(models.TextChoices):
        SUPERUSER = 'S', _('Superuser')
        ADMIN = 'A', _('Admin')
        MEMBER = 'M', _('Member')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=UserRole.choices, default=UserRole.MEMBER)


class Node(models.Model):
    class NodeStatus(models.TextChoices):
        OFFLINE = 'O', _('Offline')
        IDLE = 'I', _('Idle')
        BUSY = 'B', _('Busy')

    name = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=NodeStatus.choices, default=NodeStatus.OFFLINE)
    last_status_update = models.DateTimeField()

    def __str__(self):
        return self.name


class Board(models.Model):
    class BoardStatus(models.TextChoices):
        NOT_CONNECTED = 'N', _('Not connected')
        IDLE = 'I', _('Idle')
        BUSY = 'B', _('Busy')

    name = models.TextField()
    path = models.TextField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=BoardStatus.choices, default=BoardStatus.NOT_CONNECTED)

    def __str__(self):
        return self.name
