from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

room_validator = RegexValidator(r'^[A-Za-z0-9\s]+$', 'Room may contain only letters, numbers and spaces')# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True) #############autofield mouch kima user PK CIN
    title=models.CharField(max_length=50)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    room=models.CharField(max_length=100,validators=[room_validator])   
    conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="sessions")
    #conference=models.ForeignKey("Conference")