from django.contrib import admin
from .models import Post, Instrument, Checklist, Profile

admin.site.register(Post) # register post model
admin.site.register(Instrument) # register instrument model
admin.site.register(Checklist) # register checklist model
admin.site.register(Profile) # register profile model