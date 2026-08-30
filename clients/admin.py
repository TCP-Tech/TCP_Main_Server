from django.contrib import admin
from .models import Mentor, Mentee, Team


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'supermentor')

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('supermentor',)
        return ()


admin.site.register(Mentee)
admin.site.register(Team)
