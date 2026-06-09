from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentsUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    type = models.CharField(max_length=15,null=True)

    def __str__(self):
        return self.user.username
    
class Recruiter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    company = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=15,null=True)
    status = models.CharField(max_length=20,null=True)
    
    def __str__(self):
        return self.user.username

class Job(models.Model):

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    salary = models.CharField(max_length=50, null=True, blank=True)
    experience = models.CharField(max_length=50, null=True, blank=True)

    job_type = models.CharField(max_length=50, choices=[
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
    ])

    description = models.TextField()

    posted_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Applied")

    def __str__(self):
        return self.user.username + " - " + self.job.title
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Apply(models.Model):

    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    apply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
