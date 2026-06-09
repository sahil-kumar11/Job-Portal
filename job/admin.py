from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(StudentsUser)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(Apply)

