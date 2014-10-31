from django.contrib import admin
from .models import Project, Item, Transcript


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    pass
