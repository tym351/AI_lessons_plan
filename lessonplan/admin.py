from django.contrib import admin
from .models import LessonPlan
from django.conf import settings

admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', '教案管理')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', '教案管理')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', '教案管理后台')

@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "created_at", "updated_at")
    search_fields = ("title", "objectives", "content")
