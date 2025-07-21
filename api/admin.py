from django.contrib import admin
from .models import yrsExperience, LoginDetails,Recruiter,RecruiterArch,UsageDetails,TechInMenu,Domain,SkillsInMenu,Level,AI_Model
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(LoginDetails)
admin.site.register(Recruiter)
admin.site.register(RecruiterArch)
admin.site.register(TechInMenu)
admin.site.register(UsageDetails)
admin.site.register(SkillsInMenu)
admin.site.register(Domain)
admin.site.register(Level)
admin.site.register(AI_Model)
admin.site.register(yrsExperience)
username = "aseem"
password = "859488"

