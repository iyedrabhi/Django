from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from .forms import ConferenceModel
# Create your views here.
def all_conferences(req):
    conferences = Conference.objects.all()
    return render(req, 'conference/liste.html', {"liste": conferences})

class ConferenceList(ListView):
    model = Conference
    context_object_name= "liste"
    ordering=["start_date"]
    template_name ="conference/liste.html"

class ConferenceDetails(DetailView):
    model =Conference
    template_name ="conference/details.html"
    context_object_name ="conference"
class ConferenceCreate(CreateView):
    model=Conference
    template_name="conference/conference_form.html"
    #fields = "__all__"
    form_class = ConferenceModel
    success_url = reverse_lazy("conference_liste") #si ajout avec succes il faut aller a l'autre url
class ConferenceUpdate(UpdateView):
    model = Conference
    template_name = "conference/conference_form.html"
    #fields ="__all__"
    success_url = reverse_lazy("conference_liste") #si ajout avec succes il faut aller a l'autre url
    form_class = ConferenceModel
class ConferenceDelete(DeleteView):
    model = Conference
    template_name = "conference/conference_confirm_delete.html"
    success_url = reverse_lazy("conference_liste") #si ajout avec succes il faut aller a l'autre url

