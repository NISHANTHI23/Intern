from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('festival/', views.festival, name='festival'),
    path('offer-letter/', views.offer_letter, name='offer_letter'),
    path('birthday/', views.birthday, name='birthday'),
    path('relieving/', views.relieving, name='relieving'),
    path('office-criteria/', views.office_criteria, name='office_criteria'),
    path('attendance_record/', views.attendance_record, name='attendance_record'),
    
    
    path('enter-name/<team_name>/', views.enter_name, name='enter_name'),
    path('update-time/<int:member_id>/', views.update_time, name='update_time'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('view-all-team-data/<team_name>/', views.view_all_team_data, name='view_all_team_data'),  # New path to view all data




    
    path('', views.user_login, name='user_login'),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path('home/', views.home, name='home'),
    path('festival/', views.festival, name='festival'),




path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('change-password/', views.change_password, name='change_password'),

path('logout/', views.logout_view, name='logout'),
   
path('leave/', views.leave, name='leave'),  # Corrected name
    path('requested-forms/', views.requested_forms, name='requested_forms'),
path('update-status/<int:app_id>/', views.update_status, name='update_status'),
    path('delete-application/', views.delete_application, name='delete_application'),

    path('employee-details/', views.employee_details, name='employee_details'),

    path('details/', views.details, name='details'),  # New URL for displaying details

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
