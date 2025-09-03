from django.contrib import admin
from .models import User
from django import forms

class CustomUserAdmin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'birthday', 'bio', 'following']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = CustomUserAdmin
    list_display = ('email', 'username', 'birthday')
    readonly_fields = ('id', 'password', 'picture')
    search_fields = ('email', 'username')
    list_filter = ('birthday',)
