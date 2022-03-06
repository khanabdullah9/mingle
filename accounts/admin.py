from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AdminAccount(UserAdmin):
    list_display = ('user_id','email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('date_joined','last_login')
    ordering = ('-date_joined',)#display in descending order
    #making the password readonly on admin panel
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Account,AdminAccount)
