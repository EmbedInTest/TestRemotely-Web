from django.contrib import admin

from .models import Organization, Node, Board

admin.site.register(Organization)
admin.site.register(Node)
admin.site.register(Board)
