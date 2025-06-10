# admin.py
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'complete', 'duedate')
    list_filter = ('complete', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'duedate'