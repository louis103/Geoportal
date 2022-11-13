from django.contrib import admin

# Register your models here.
from .models import Profile, GisData, SendMessage

admin.site.register(Profile)
admin.site.register(GisData)
admin.site.register(SendMessage)

