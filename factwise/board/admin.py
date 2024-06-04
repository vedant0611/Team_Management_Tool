from django.contrib import admin

# Register your models here.
from django.contrib import admin
from board.models import Board, Task

# Register your models here.
admin.site.register(Board)
admin.site.register(Task)