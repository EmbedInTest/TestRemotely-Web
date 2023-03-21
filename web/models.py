import datetime

from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager


class Organization(models.Model):
    name = models.TextField()
    members = models.ManyToManyField(User, through="UserMembership")

    def __str__(self):
        return f"(org: {self.name})"


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
    owner = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)

    def __str__(self):
        return f"(device: {self.name} from {self.owner})"


class Board(models.Model):
    name = models.TextField()
    path = models.TextField()
    device = models.ForeignKey(Device, related_name='boards', on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return f"(board: {self.name}, device: {self.device})"


class BoardStatus(models.Model):
    class eBoardStatus(models.TextChoices):
        NOT_CONNECTED = 'N', _('Not connected')
        CONNECTED = 'C', _('connected')

    board = models.ForeignKey(Board, related_name='status', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=eBoardStatus.choices, default=eBoardStatus.NOT_CONNECTED)
    last_update = models.DateTimeField()

    def __str__(self):
        return f"(board status: {self.board}, status: {self.status}, last update: {self.last_update})"


class Run(models.Model):
    triggerer = models.ForeignKey(User, related_name='runs', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    tags = TaggableManager()
    dispatched_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"(run: triggerer: {self.triggerer}, dispatched at: {self.dispatched_at})"


class RunStatus(models.Model):
    class eRunStatus(models.TextChoices):
        RUNNING = 'R', _('Running')
        DONE = 'D', _('Done')

    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=eRunStatus.choices, default=eRunStatus.RUNNING)
    last_update = models.DateTimeField()

    def __str__(self):
        return f"(run status: {self.run}, status: {self.status}, last update: {self.last_update})"


class Run2Board(models.Model):
    board = models.ForeignKey(Board, related_name='run', on_delete=models.CASCADE)
    run = models.ForeignKey(Run, related_name='board', on_delete=models.CASCADE)
    last_update = models.DateTimeField()

    def __str__(self):
        return f"(board status: {self.board}, run: {self.run}, last update: {self.last_update})"
