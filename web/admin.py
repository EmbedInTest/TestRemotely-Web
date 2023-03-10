from django.contrib import admin

from .models import Organization, UserMembership, Device, Board, BoardStatus, Run

admin.site.register(Organization)
admin.site.register(UserMembership)
admin.site.register(Device)
admin.site.register(Board)
admin.site.register(BoardStatus)
admin.site.register(Run)
