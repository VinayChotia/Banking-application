from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# class CustomUserAdmin(UserAdmin):
#     model = User
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('user_id', 'user_type', 'kyc_status')}),
#     )

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Account)