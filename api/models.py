from django.db import models
from django.contrib.auth.models import User
class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    upload = models.FileField(upload_to='uploads/')
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.user.username

class LoginDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # You can hash this manually
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'login_details'
class Recruiter(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    dOB = models.CharField(max_length=255)
    dOJ = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pNumber = models.CharField(max_length=255)
    address =  models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    class Meta:
        db_table = 'recruiter'
class RecruiterArch(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    dOB = models.CharField(max_length=255)
    dOJ = models.CharField(max_length=255)
    dOL = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pNumber = models.CharField(max_length=255)
    address =  models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    class Meta:
        db_table = 'recruiter_archive'

class UsageDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    usageDateTime = models.DateTimeField()
    techOpt = models.CharField(max_length=255)
    skillOpt = models.CharField(max_length=255)
    file_1 = models.FileField(null=True)
    file_2=models.FileField(null=True)
    class Meta:
        db_table = 'usage_details'

class TechInMenu(models.Model):
    techId = models.AutoField(primary_key=True)
    techName = models.CharField(max_length=255)
    techDescription = models.TextField()
    class Meta:
        db_table = 'techinmenu'
class Domain(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domainName = models.CharField(max_length=255)
    domainDescription = models.TextField()
    class Meta:
        db_table = 'domaininmenu'

class Level(models.Model):
    levelId = models.AutoField(primary_key=True)
    levelName = models.CharField(max_length=255)
    levelDescription = models.TextField()
    class Meta:
        db_table = 'levelinmenu'
class SkillsInMenu(models.Model):
    skillID = models.AutoField(primary_key=True)
    skillName=models.CharField(max_length=255)
    skillDescription=models.TextField()
    class Meta:
        db_table = 'skillsinmenu'
class AI_Model(models.Model):
    modelId = models.AutoField(primary_key=True)
    modelName = models.CharField(max_length=255)
    techDescription = models.TextField()
    class Meta:
        db_table = 'modelinmenu'
class yrsExperience(models.Model):
    yrsId = models.AutoField(primary_key=True)
    yrsexp = models.CharField(max_length=255)
    class Meta:
        db_table='yrsexp'



