from django.contrib import admin
from userauths.models import Profile, User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender', 'country']
    # list_editable = ['gender', 'country'] #remove the first field toavoid getting an error
    # search_fields = ['full_name', ]
    # list_filter = ['date']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
