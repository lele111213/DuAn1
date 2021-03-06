from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import BillPay
from .forms import UserAdminCreationForm, UserAdminChangeForm
# Register your models here.
User = get_user_model()
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['username', 'fullname', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('fullname', 'phonenumber', 'addressId', 'addressName', 'gender', 'age', 'height', 'hobbies', 'image', 'channel', 'room_chat', 'room_view')}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname', 'phonenumber', 'addressId', 'addressName', 'gender', 'age','height', 'hobbies', 'image', 'password1', 'password2', 'admin', 'staff', 'active')}
        ),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal = ()


admin.site.register(User, UserAdmin),
admin.site.register(BillPay)