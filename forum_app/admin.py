from django.contrib import admin

from .models import Section, Thread, Post


admin.site.register(Section)
admin.site.register(Thread)
admin.site.register(Post)
# Register your models here.
