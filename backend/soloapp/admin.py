from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Unit

class EmployeeAdmin(UserAdmin):
    model = Employee
    list_display = ('NTID', 'Email_Id', 'First_Name', 'Last_Name', 'is_staff')
    search_fields = ('NTID', 'Email_Id')
    ordering = ('NTID',)

    fieldsets = (
        (None, {'fields': ('NTID', 'password')}),
        ('Personal info', {'fields': ('First_Name', 'Last_Name', 'Email_Id', 'Unit_Name', 'PhotoFileName')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Unit)

# Register your models here.
