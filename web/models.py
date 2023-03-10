from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager


class Organization(models.Model):
    name = models.TextField()
    members = models.ManyToManyField(User, through="UserMembership")

    def __str__(self):
        return self.name.__str__()


class UserMembership(models.Model):
    class UserRole(models.TextChoices):
        SUPERUSER = 'S', _('Superuser')
        ADMIN = 'A', _('Admin')
        MEMBER = 'M', _('Member')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=UserRole.choices, default=UserRole.MEMBER)


class Device(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.__str__()


class Board(models.Model):
    name = models.TextField()
    path = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.name.__str__()


class BoardStatus(models.Model):
    class eBoardStatus(models.TextChoices):
        NOT_CONNECTED = 'N', _('Not connected')
        IDLE = 'I', _('Idle')
        BUSY = 'B', _('Busy')

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=eBoardStatus.choices, default=eBoardStatus.NOT_CONNECTED)
    last_update = models.DateTimeField()


class Run(models.Model):
    class eRunStatus(models.TextChoices):
        WAITING = 'W', _('Waiting')
        RUNNING = 'R', _('Running')
        DONE = 'D', _('Done')

    board_status = models.ForeignKey(BoardStatus, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1, choices=eRunStatus.choices, default=eRunStatus.WAITING)
    file = models.FileField(upload_to='uploads/')
    tags = TaggableManager()
