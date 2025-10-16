from django.contrib import admin
from .models import Submission, Conference
# Register your models here.
admin.site.register(Submission)
admin.site.site_header="CONFIRINCE MANAJMENT ADDMIN 25/26"
admin.site.index_title="CONFIRANS"
admin.site.site_title="CONFIRANS MANAJMNT"

@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")
    ordering = ("start_date",)
    list_filter = ("theme", "location", "end_date")
    search_fields = ("name",)
    
    fieldsets = (
        ("Information General", {
            "fields": (
                "conference_id",
                "name",
                "theme",
                "description",
            )
        }),
        ("Logistics", {
            "fields": (
                "location",
                "start_date",
                "end_date",
            )
        }),
    )
    
    readonly_fields = ("conference_id",)

    # Custom method to calculate duration
    def duration(self, objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date - objet.start_date).days
        return "RAS"
    
    duration.short_description = "Duration (days)"