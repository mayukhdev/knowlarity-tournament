from django.contrib import admin

from .models import Sport, Team, Employee
# Register your models here.

admin.site.register(Sport)
admin.site.register(Team)
admin.site.register(Employee)
