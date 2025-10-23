from django.urls import path
from .views import *
#from . import views
urlpatterns = [
    #path("liste/",views.all_conferences,name="conference_liste"), #############5ater bech ne5dem bel base louta
    path("liste/",ConferenceList.as_view(),name="conference_liste"),
    path("details/<int:pk>/",ConferenceDetails.as_view(),name="conference_detail"),
    path("form/", ConferenceCreate.as_view(), name="conference_add"),


]