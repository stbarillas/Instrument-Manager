from django.contrib import admin
from .models import Post, Instrument, Checklist, Profile

admin.site.register(Post)
admin.site.register(Instrument)
admin.site.register(Checklist)
admin.site.register(Profile)