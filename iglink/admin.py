from django.contrib import admin

from .forms import IGApiForm
from .models import InstagramAPISettings


@admin.register(InstagramAPISettings)
class InstagramAPIModelAdmin(admin.ModelAdmin):
    """
    Input Instagram username.
    """
    form = IGApiForm
    list_display = ("ig_username",)
