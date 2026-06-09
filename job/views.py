from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def index(request):
    return render(request,'index.html')


def admin_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            error = "no"   # success
        else:
            error = "yes"  # fail

    return render(request, 'admin_login.html', {'error': error})

def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful 🎉")
            return redirect('user_home')

        else:
            messages.error(request, "Invalid Username or Password ❌")
            return redirect('user_login')

    return render(request, 'user_login.html')

def recruiter_login(request):

    error = ""

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:

            login(request, user)

            error = "no"

        else:

            error = "yes"

    return render(request, 'recruiter_login.html', {'error':error})



def recruiter_signup(request):

    error = ""

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        company = request.POST['company']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        password = request.POST['password']
        image = request.FILES['image']

        try:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            Recruiter.objects.create(
                user=user,
                mobile=mobile,
                image=image,
                gender=gender,
                company=company,
                type="recruiter",
                status="pending"
            )

            error = "no"

        except:

            error = "yes"

    return render(request, 'recruiter_signup.html', {'error':error})

def user_signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('user_login')

    return render(request, 'user_signup.html')


def user_logout(request):
    logout(request)
    return redirect('index')

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'user_home.html')

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    return render(request, 'recruiter_home.html')

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')


def view_users(request):
    users = User.objects.all()
    return render(request, 'view_users.html', {'users': users})

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('view_users')

def view_all_recruiters(request):
    data = Recruiter.objects.all()
    return render(request, "view_all_recruiters.html", {"data": data})

def view_pending_recruiters(request):
    data = Recruiter.objects.filter(status="pending")
    return render(request, "view_pending_recruiters.html", {"data": data})

def view_accepted_recruiters(request):
    data = Recruiter.objects.filter(status="accepted")
    return render(request, "view_accepted_recruiters.html", {"data": data})

def view_rejected_recruiters(request):
    data = Recruiter.objects.filter(status="rejected")
    return render(request, "view_rejected_recruiters.html", {"data": data})

def accept_recruiter(request, id):
    recruiter = Recruiter.objects.get(id=id)
    recruiter.status = "accepted"
    recruiter.save()
    return redirect('recruiter_list_pending')

def reject_recruiter(request, id):
    recruiter = Recruiter.objects.get(id=id)
    recruiter.status = "rejected"
    recruiter.save()
    return redirect('recruiter_list_pending')

def delete_recruiter(request, id):
    rec = Recruiter.objects.get(id=id)
    rec.delete()
    return redirect('recruiter_list_all')


@login_required
def recruiter_home(request):
    error = ""

    recruiter = Recruiter.objects.filter(user=request.user).first()

    if request.method == "POST":

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact = request.POST['contact']
        gender = request.POST['gender']

        if recruiter:
            recruiter.first_name = first_name
            recruiter.last_name = last_name
            recruiter.contact = contact
            recruiter.gender = gender
            recruiter.save()
        else:
            Recruiter.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                contact=contact,
                gender=gender
            )

        error = "no"

    return render(request, "recruiter_home.html", {'recruiter': recruiter, 'error': error})

def add_job(request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""

    if request.method == "POST":

        title = request.POST['title']
        company = request.POST['company']
        location = request.POST['location']
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')
        job_type = request.POST['job_type']
        description = request.POST['description']

        # create job
        Job.objects.create(
            recruiter=request.user,
            title=title,
            company=company,
            location=location,
            salary=salary,
            experience=experience,
            job_type=job_type,
            description=description,
        )

        error = "no"

    return render(request, 'add_job.html', {'error': error})

def recruiter_job_list(request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    jobs = Job.objects.filter(recruiter=request.user).order_by('-posted_on')

    return render(request, 'recruiter_job_list.html', {'jobs': jobs})

def applied_candidates(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    # Get all jobs posted by this recruiter
    recruiter_jobs = Job.objects.filter(recruiter=request.user)
    
    # Use Apply model instead of Application
    applications = Apply.objects.filter(
        job__in=recruiter_jobs
    ).order_by('-apply_date')
    
    return render(request, 'applied_candidates.html', {
        'applications': applications
    })

def recruiter_change_password(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""

    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        user = authenticate(username=request.user.username, password=old_password)

        if user is not None:
            user.set_password(new_password)
            user.save()
            error = "no"
        else:
            error = "yes"

    return render(request, 'recruiter_change_password.html', {'error': error})

def recruiter_logout(request):
    logout(request)
    return redirect('recruiter_login')

def admin_change_password(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')

    error = ""

    if request.method == "POST":

        old = request.POST['old_password']
        new = request.POST['new_password']

        user = authenticate(username=request.user.username, password=old)

        if user:
            user.set_password(new)
            user.save()
            error = "no"
        else:
            error = "yes"

    return render(request, 'admin_change_password.html', {'error': error})

def user_change_password(request):

    if not request.user.is_authenticated:
        return redirect('user_login')

    error = ""

    if request.method == "POST":

        old = request.POST['old_password']
        new = request.POST['new_password']

        user = authenticate(username=request.user.username, password=old)

        if user:
            user.set_password(new)
            user.save()
            error = "no"
        else:
            error = "yes"

    return render(request, 'user_change_password.html', {'error': error})

def recruiter_change_password(request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""

    if request.method == "POST":

        old = request.POST['old_password']
        new = request.POST['new_password']

        user = authenticate(username=request.user.username, password=old)

        if user:
            user.set_password(new)
            user.save()
            error = "no"
        else:
            error = "yes"

    return render(request, 'recruiter_change_password.html', {'error': error})

def latest_jobs(request):

    jobs = Job.objects.filter(status="Active").order_by('-posted_on')

    return render(request, "latest_jobs.html", {'jobs': jobs})

def contact(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Message sent successfully!")

    return render(request, "contact.html")


def job_list(request):

    jobs = Job.objects.filter(status="Active")

    search = request.GET.get('search')

    if search:
        jobs = jobs.filter(title__icontains=search)

    context = {
        'jobs': jobs
    }

    return render(request, 'job_list.html', context)

@login_required
def apply_job(request, id):

    job = Job.objects.get(id=id)

    application, created = Apply.objects.get_or_create(
        job=job,
        user=request.user
    )

    if created:
        return render(request, 'apply_job.html', {'status': 'success'})
    else:
        return render(request, 'apply_job.html', {'status': 'already'})

def applied_jobs(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    # Use Apply model
    jobs = Apply.objects.filter(user=request.user).order_by('-apply_date')
    
    return render(request, 'applied_jobs.html', {'jobs': jobs})

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    error = ""
    success = ""
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Check if username already exists (excluding current user)
        if User.objects.exclude(id=request.user.id).filter(username=username).exists():
            error = "Username already taken!"
        elif User.objects.exclude(id=request.user.id).filter(email=email).exists():
            error = "Email already registered!"
        else:
            # Update user details
            user = request.user
            user.username = username
            user.email = email
            user.save()
            success = "Profile updated successfully!"
    
    return render(request, 'user_profile.html', {
        'error': error,
        'success': success
    })

def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('recruiter_job_list')