from django.db import models
from django.contrib.auth.models import AbstractUser ########Bech tjib abstractuser 7adher
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
import uuid
def generate_userid():
    return "USER"+uuid.uuid4().hex[:4].upper()
def verify_email(email):
    domaine=["esprit.tn","sesame.com","tek.tn","central.com"]
    if email.split("@")[1] not in domaine:
        raise ValidationError("l'email est invalide et appartenir a un domaine universitaire")
    
name_validator = RegexValidator (
    regex=r'^[A-Za-z\s-]+$' ####### EXPRESSION REGULIER regex=r'[A-Za-z\s-]+' MATEMCHICH FOR SOME REASON
)
    

class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    first_name=models.CharField(max_length=50,validators=[name_validator])
    last_name=models.CharField(max_length=50,validators=[name_validator])
    email=models.EmailField(unique=True,validators=[verify_email])
    affiliation=models.CharField(max_length=50)
    nationality=models.CharField(max_length=50)
    ROLE=[
        ("participant","Participant"),
        ("commitee","Organizing commitee member")

    ]
    role=models.CharField(max_length=50,choices=ROLE,default="Participant")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #submissions=models.ManyToManyField("ConferenceApp.Conference",through="Submission")
    #OrganizingCommiteeList=models.ManyToManyField("ConferenceApp.Conference",through="OrganizingCommitee")
    def save(self,*args,**kwargs):###########Fonc save tbadel fel user#args kif nabda manaarech number args, ki yabda andi args bel cle..
        if not self.user_id:
            new_id=generate_userid()
            while User.objects.filter(user_id=new_id).exists():
                new_id=generate_userid()
            self.user_id=new_id
        super().save(*args,**kwargs)
class OrganizingCommitee(models.Model):
    user=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name="commitees")
    conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="commitees")
    ROLES=[
        ("chair","Chair"),
        ("co-chair","Co-chair"),
        ("member","Member")
    ]
    commitee_role=models.CharField(max_length=50,choices=ROLES)
    date_join=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)