from django.contrib import admin
from .models import Submission, Conference


# -----------------------------
# 🔧 Personnalisation de l'interface globale
# -----------------------------
admin.site.site_header = "CONFÉRENCE MANAGEMENT ADMIN 25/26"
admin.site.index_title = "Gestion des conférences"
admin.site.site_title = "Admin Conférences"


# -----------------------------
# 🏛️ ADMIN DE CONFERENCE
# -----------------------------
@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    # a. Colonnes affichées
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")

    # g. Tri
    ordering = ("start_date",)

    # d. Filtres
    list_filter = ("theme", "location", "start_date")

    # e. Recherche
    search_fields = ("name", "description", "location")

    # f. Fieldsets
    fieldsets = (
        ("Informations générales", {
            "fields": ("conference_id", "name", "theme", "description"),
        }),
        ("Logistique", {
            "fields": ("location", "start_date", "end_date"),
        }),
    )

    # h. Lecture seule
    readonly_fields = ("conference_id",)

    # b. Méthode durée
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "N/A"
    duration.short_description = "Durée (jours)"

    # h. Navigation par calendrier
    date_hierarchy = "start_date"


# -----------------------------
# 📄 ADMIN DE SUBMISSION
# -----------------------------
@admin.action(description="Marquer comme payé")
def mark_as_payed(modeladmin, request, queryset):
    queryset.update(payed=True)
@admin.action
def mark_as_accepted(m,req,q):
    q.update(status="accepted")

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    # a. Colonnes
    list_display = ("title", "status", "user_id", "conference", "submission_date", "payed")

    # d. Filtres
    list_filter = ("status", "payed", "conference", "submission_date")

    # e. Recherche
    search_fields = ("title", "keyword", "user_id__username")

    # f. Édition directe
    list_editable = ("status", "payed")

    # g. Fieldsets
    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstract", "keyword"),
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference"),
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user_id"),
        }),
    )

    # h. Lecture seule
    readonly_fields = ("submission_id", "submission_date")

    # Action personnalisée
    actions = [mark_as_payed,mark_as_accepted]
