from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here
from .models import Human

# Define an inline admin descriptor for Human model
# which acts a bit like a singleton.
# See https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
class HumanInline(admin.StackedInline):
    model = Human
    can_delete = False
    verbose_name_plural = 'human'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (HumanInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
