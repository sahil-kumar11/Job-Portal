"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job.views import*
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('admin_login/',admin_login,name='admin_login'),
    path('user_login/',user_login,name='user_login'),
    path('recruiter_login/',recruiter_login,name='recruiter_login'),
    path('user_signup/',user_signup,name='user_signup'),
    path('user_logout/', user_logout, name='user_logout'),
    path('user_home/', user_home, name='user_home'),
    path('recruiter_signup/', recruiter_signup, name='recruiter_signup'),
    path('recruiter_home/', recruiter_home, name='recruiter_home'),
    path('admin_home/',admin_home,name="admin_home"),
    path('view_users/', view_users, name='view_users'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),
    path('recruiters/pending/', view_pending_recruiters, name='recruiter_list_pending'),
    path('recruiters/accepted/', view_accepted_recruiters, name='recruiter_list_accepted'),
    path('recruiters/rejected/', view_rejected_recruiters, name='recruiter_list_rejected'),
    path('recruiter/accept/<int:id>/', accept_recruiter, name='accept_recruiter'),
    path('recruiter/reject/<int:id>/', reject_recruiter, name='reject_recruiter'),
    path('recruiters/all/', view_all_recruiters, name='recruiter_list_all'),
    path('recruiters/delete/<int:id>/', delete_recruiter, name='delete_recruiter'),
    path('recruiter_home/', recruiter_home, name='recruiter_home'),
    path('add_job/', add_job, name='add_job'),
    path('recruiter_job_list/', recruiter_job_list, name='recruiter_job_list'),
    path('applied_candidates/', applied_candidates, name='applied_candidates'),
    path('recruiter_change_password/', recruiter_change_password, name='recruiter_change_password'),
    path('recruiter_logout/', recruiter_logout, name='recruiter_logout'),
    path('admin_change_password/', admin_change_password, name='admin_change_password'),
    path('user_change_password/', user_change_password, name='user_change_password'),
    path('latest_jobs/', latest_jobs, name='latest_jobs'),
    path('apply_job/<int:id>/', apply_job, name='apply_job'),
    path('contact/', contact, name='contact'),
    path('job_list/', job_list, name='job_list'),
    path('applied_jobs/', applied_jobs, name='applied_jobs'),
    path('user_profile/', user_profile, name='user_profile'),
    path('delete_job/<int:id>/', delete_job, name='delete_job'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
