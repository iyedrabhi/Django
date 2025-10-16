from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
#from ConferenceApp.models import Conference
# Create your models here.
    
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True) #############autofield wala increment mouch kima user PK CIN
    name=models.CharField(max_length=50)
    description=models.TextField(validators=[MinLengthValidator(limit_value=30,message="la description doit contenir au minimum 30 caractères")])
    location=models.CharField(max_length=50)
    THEME=[
        ("CS&IA","Computer science & IA"),
        ("CS","Social science"),
        ("SE","Science and eng")
    ]
    theme=models.CharField(max_length=50,choices=THEME)
    start_date = models.DateField()
    end_date = models.DateField()
    def clean(self):
        if self.start_date > self.end_date :
            raise ValidationError("la date debut doit etre anterieur")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} - {self.theme} ({self.start_date} to {self.end_date})"
    

class Submission(models.Model):
    submission_id=models.CharField(primary_key=True,max_length=50,unique=True)
    user_id=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name="submissions")
    conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="submissions")
    title=models.CharField(max_length=50)
    abstract=models.TextField()
    keyword=models.TextField()
    paper = models.FileField(upload_to='sub_paper/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])    
    CHOICES=[
        ("submitted","Submitted"),
        ("under review","Under review"),
        ("rejected","Rejected"),
        ("accepted","Accepted")
    ]
    status=models.CharField(max_length=50,choices=CHOICES)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)