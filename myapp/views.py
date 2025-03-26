
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Festival
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse
from .models import TeamMember, TimeEntry
from django.utils import timezone
import datetime
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Festival
from .models import OfferLetter
from .models import Rule
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import OfferLetter
from django.contrib.auth.decorators import login_required
import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Rule
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import TeamMember, TimeEntry
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import TeamMember, TimeEntry
import datetime
from django.utils import timezone


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def user_login(request):
    error = None  # Error message for invalid credentials

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Redirect to home page
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})



def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")  
        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken"})
        user = User.objects.create_user(username=username, password=password)
        group, created = Group.objects.get_or_create(name=role)  
        user.groups.add(group) 
        user_profile = UserProfile.objects.create(user=user, role=role)
        user.save()  
        user_profile.save()  
        return redirect("login")  
    return render(request, "register.html")



class FestivalView(LoginRequiredMixin, View):
    login_url = '/login/'  
    def get(self, request):
        festivals = Festival.objects.all()
        return render(request, 'festival.html', {'festivals': festivals})
    def post(self, request):
        if request.method == 'POST':
            if request.user.is_superuser:
                festival_name = request.POST.get('festival-name')
                festival_date = request.POST.get('festival-date')
                if festival_name and festival_date:
                    Festival.objects.create(name=festival_name, date=festival_date)
                    return redirect('festival')  
            delete_festival_id = request.POST.get('delete-festival-id')
            if request.user.is_superuser and delete_festival_id: 
                festival = get_object_or_404(Festival, id=delete_festival_id)
                festival.delete()
                return redirect('festival') 

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def festival(request):
    return render(request, 'festival.html')

def offer_letter(request):
    return render(request, 'offer_letter.html')

def birthday(request):
    return render(request, 'birthday.html')

def relieving(request):
    return render(request, 'relieving.html')

def office_criteria(request):
    return render(request, 'office_criteria.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee

@login_required
def birthday(request):
    if request.method == "POST":
        if 'delete-employee-id' in request.POST:
            # Handle deletion
            employee_id = request.POST['delete-employee-id']
            employee = get_object_or_404(Employee, id=employee_id)
            employee.delete()
            return redirect('birthday')

        # Handle form submission manually
        name = request.POST.get('name')
        department = request.POST.get('department')
        birthday = request.POST.get('birthday')

        if name and department and birthday:  # Basic validation
            Employee.objects.create(name=name, department=department, birthday=birthday)
            return redirect('birthday')

    employees = Employee.objects.all()
    return render(request, 'birthday.html', {'employees': employees})


def festival(request):
    if request.method == 'POST':
        festival_name = request.POST.get('festival-name')
        festival_date = request.POST.get('festival-date')
        if festival_name and festival_date:
            Festival.objects.create(name=festival_name, date=festival_date)
            return redirect('festival')  
        delete_festival_id = request.POST.get('delete-festival-id')
        if delete_festival_id:
            festival = get_object_or_404(Festival, id=delete_festival_id)
            festival.delete()
            return redirect('festival')  
    festivals = Festival.objects.all()
    return render(request, 'festival.html', {'festivals': festivals})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import os
from .models import OfferLetter  # Ensure your model is imported

@login_required
def offer_letter(request):
    if request.user.is_superuser:
        offer_letters = OfferLetter.objects.all()  # Admins see all offer letters
    else:
        offer_letters = OfferLetter.objects.filter(name=request.user.username)  # Match username instead of full name

    if request.method == 'POST':
        if 'name' in request.POST and 'department' in request.POST and 'offer_letter' in request.FILES:
            if request.user.is_superuser:  # Only admins can add offer letters
                name = request.POST.get('name')
                department = request.POST.get('department')
                offer_letter_file = request.FILES.get('offer_letter')
                if name and department and offer_letter_file:
                    OfferLetter.objects.create(
                        name=name,
                        department=department,
                        offer_letter=offer_letter_file
                    )
                    return redirect('offer_letter')

        if 'delete-offer-id' in request.POST:
            if request.user.is_superuser:  # Only admins can delete offer letters
                delete_offer_id = request.POST.get('delete-offer-id')
                if delete_offer_id:
                    offer = get_object_or_404(OfferLetter, id=delete_offer_id)
                    if os.path.exists(offer.offer_letter.path):
                        os.remove(offer.offer_letter.path)
                    offer.delete()
                    return redirect('offer_letter')

    return render(request, 'offer_letter.html', {'offer_letters': offer_letters})

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os

def office_criteria(request):
    if request.method == "POST":
        text_data = request.POST.get("text_data", "").strip()
        agreement = request.POST.get("agreement", "")
        uploaded_file = request.FILES.get("uploaded_file")
        request_reason = request.POST.get("request_reason", "Request for offer letter.")

        # Get logged-in user's details
        if request.user.is_authenticated:
            user_name = request.user.get_full_name() or request.user.username
        else:
            user_name = "Unknown User"

        # Handle file upload (if exists)
        file_path = None
        if uploaded_file:
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)
            file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # Check if "Request for Offer Letter" was clicked
        if agreement == "agree":
            subject = "📄 Offer Letter Request"
            message = (
                f"🔹 Employee Name: {user_name}\n"
                f"📝 Message: {text_data}\n"
                f"📧 Request Reason: {request_reason}\n"
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.COMPANY_EMAIL]  # Admin email

            # Send email with attachment
            email = EmailMessage(subject, message, from_email, recipient_list)
            if uploaded_file:
                email.attach_file(file_full_path)  # Attach uploaded file

            try:
                email.send()
                messages.success(request, "Request submitted successfully! Email sent with attachment.")
            except Exception as e:
                messages.error(request, f"Email failed to send: {str(e)}")

        return redirect("office_criteria")  # Redirect to avoid form resubmission

    return render(request, "office_criteria.html")




def attendance_record(request):
    return render(request, 'attendance_record.html')


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('view_all_team_data', team_name=kwargs.get('team_name'))
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view)

@admin_required
def enter_name(request, team_name):
    message = ""  
    
    if request.method == 'POST':
        name = request.POST.get('team-name')

        if name:
            team_member = TeamMember(team_name=team_name, member_name=name)
            team_member.save()  
            message = f"{name} has been added to the {team_name}."
        else:
            message = "Please enter a name."

    members = TeamMember.objects.filter(team_name=team_name)
    
    for member in members:
        latest_time_entry = member.time_entries.latest('time_in') if member.time_entries.exists() else None
        member.latest_time_entry = latest_time_entry

    return render(request, 'enter_name.html', {'team_name': team_name, 'message': message, 'members': members})



def update_time(request, member_id):
    if request.method == 'POST':
        member = TeamMember.objects.get(id=member_id)
        new_time = request.POST.get('time-in')

        if new_time:
            time_in = timezone.datetime.strptime(new_time, "%Y-%m-%dT%H:%M")

            TimeEntry.objects.create(member=member, time_in=time_in)

        return redirect('enter_name', team_name=member.team_name)

def delete_member(request, member_id):
    try:
        team_member = TeamMember.objects.get(id=member_id)
        team_member.delete()
    except TeamMember.DoesNotExist:
        pass  

    return redirect('enter_name', team_name=team_member.team_name)







@login_required
def view_all_team_data(request, team_name):
    logged_in_username = request.user.username

    # Check if the logged-in user is an admin
    if request.user.is_staff:
        # Admin can view all members in the team
        members = TeamMember.objects.filter(team_name=team_name)
    else:
        # Non-admin user can only view their own data
        members = TeamMember.objects.filter(team_name=team_name, member_name=logged_in_username)

    # If no members found for the team
    if not members:
        # You can handle this case by showing an error message
        return render(request, 'error_page.html', {'message': "No team members found for this team."})

    # Prepare the data for each member
    member_data = []
    for member in members:
        # Get time entries for each member
        time_entries = member.time_entries.all()
        member_info = []
        late_count = 0  # To track late entries for summary

        for entry in time_entries:
            # Set the office start time to 9:00 AM
            office_start_time = datetime.datetime(entry.time_in.year, entry.time_in.month, entry.time_in.day, 9, 0, 0)

            # Make sure it's timezone aware
            office_start_time = timezone.make_aware(office_start_time, timezone.get_current_timezone())  

            # Calculate how many minutes late the member is
            late_minutes = (entry.time_in - office_start_time).total_seconds() / 60

            # If late, calculate the deduction time (30 minutes for every 10 minutes late)
            if late_minutes > 0:
                # Calculate how many 10-minute intervals of lateness
                deduction_minutes = (int(late_minutes) // 10) * 40

                # Calculate the deduction time by adding deduction to 9:00 AM
                deduction_time = office_start_time + datetime.timedelta(minutes=deduction_minutes)

                late_str = f"Late ({str(datetime.timedelta(minutes=late_minutes))})"
                deduction_str = deduction_time.strftime('%H:%M:%S')  # Deduction time in HH:MM:SS format
                late_count += 1  # Increment late entry count
            else:
                deduction_minutes = 0  # No deduction if on time
                late_str = "On Time"
                deduction_str = office_start_time.strftime('%H:%M:%S')  # No deduction, so just show the office time

            # Append time entry information to the member's list
            member_info.append({
                'time_in': entry.time_in.strftime('%Y-%m-%d %H:%M'),  # Keep time_in to show when the member clocked in
                'late_str': late_str,
                'deduction_time': deduction_str  
            })
        member_data.append({
            'member': member,
            'time_info': member_info,
            'late_count': late_count, 
        })
    return render(request, 'view_all_team_data.html', {'team_name': team_name, 'member_data': member_data})



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip() 
        user = User.objects.filter(email=email).first()  
        if not user:
            return render(request, 'forgot_password.html', {'error': 'Email not found.'})
        otp_code = random.randint(100000, 999999) 
        request.session['otp_code'] = otp_code  
        request.session['user_id'] = user.id   
        subject = 'Your OTP for Password Reset'
        message = f'Your OTP code is {otp_code}. This is a company-wide email.'
        email_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.COMPANY_EMAIL])
        if email_sent:
            print(f"OTP email sent successfully to {settings.COMPANY_EMAIL}")
            return redirect('otp_verification')  
        else:
            return render(request, 'forgot_password.html', {'error': 'Failed to send OTP. Try again.'})
    return render(request, 'forgot_password.html')



def otp_verification(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        stored_otp = request.session.get('otp_code')
        if str(otp_code) == str(stored_otp):
            return redirect('change_password')  
        else:
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP.'})
    return render(request, 'otp_verification.html')


def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        username = request.POST.get('username')  
        if new_password != confirm_password:
            return render(request, 'change_password.html', {'error': 'Passwords do not match.'})

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            user = authenticate(username=username, password=new_password)
            if user is not None:
                login(request, user)
                return redirect('login')  
            else:
                return render(request, 'change_password.html', {'error': 'Authentication failed with new password.'})
        except User.DoesNotExist:
            return render(request, 'change_password.html', {'error': 'User not found.'})
    return render(request, 'change_password.html')



def logout_view(request):
    logout(request)
    return redirect('login')  



from django.shortcuts import render, redirect
















from django.shortcuts import render, redirect
from .models import PermissionApplication, LeaveApplication
def leave(request):
    if request.user.is_staff:
        return redirect('requested_forms')
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'permission_form':
            permission_app = PermissionApplication(
                date=request.POST.get('date'),
                name=request.POST.get('name'),
                designation=request.POST.get('designation'),
                emp_code=request.POST.get('emp_code'),
                permission_from=request.POST.get('Permission_from'),
                permission_till=request.POST.get('Permission_till'),
                no_of_hours=request.POST.get('no_of_hours'),
                purpose=request.POST.get('purpose'),
                permission_on=request.POST.get('permission_on'),
            )
            permission_app.save()
        elif form_type == 'leave_form':
            leave_app = LeaveApplication(
                date=request.POST.get('date'),
                name=request.POST.get('name'),
                designation=request.POST.get('designation'),
                emp_code=request.POST.get('emp_code'),
                leave_from=request.POST.get('Leave_from'),
                leave_till=request.POST.get('Leave_till'),
                no_of_days=request.POST.get('no_of_days'),
                purpose=request.POST.get('purpose'),
                leave_on=request.POST.get('leave_on'),
            )
            leave_app.save()

        return redirect('requested_forms')  # Redirect to the requested forms page
    return render(request, 'leave.html')  # If it's a GET request, just render the form page


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PermissionApplication, LeaveApplication
from django.shortcuts import render, redirect, get_object_or_404
from .models import PermissionApplication, LeaveApplication

from django.shortcuts import render, redirect, get_object_or_404
from .models import PermissionApplication, LeaveApplication

def requested_forms(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    # Fetch permission and leave applications
    if request.user.is_superuser:
        # If the user is an admin (superuser), show all applications
        permission_apps = PermissionApplication.objects.all()
        leave_apps = LeaveApplication.objects.all()
    else:
        # If the user is not an admin, show only their own applications
        permission_apps = PermissionApplication.objects.filter(name=request.user.username)
        leave_apps = LeaveApplication.objects.filter(name=request.user.username)

    # Process form submissions
    if request.method == 'POST':
        app_id = request.POST.get('app_id')  # Get the application ID
        comment = request.POST.get('comment')  # Get the comment (which will be the status)
        app_type = request.POST.get('app_type')  # Check if it's 'permission' or 'leave'

        if app_type == 'permission':
            # Fetch the corresponding PermissionApplication
            app = get_object_or_404(PermissionApplication, id=app_id)
        elif app_type == 'leave':
            # Fetch the corresponding LeaveApplication
            app = get_object_or_404(LeaveApplication, id=app_id)
        else:
            return redirect('requested_forms')  # In case of an invalid app_type

        # Update the status with the comment
        app.status = comment
        app.save()  # Save the updated status

        return redirect('requested_forms')  # Redirect after updating

    return render(request, 'requested_forms.html', {
        'permission_apps': permission_apps,
        'leave_apps': leave_apps,
    })




from django.shortcuts import render, redirect, get_object_or_404
from .models import PermissionApplication, LeaveApplication
from django.contrib.auth.decorators import login_required

@login_required
def delete_application(request):
    if request.method == "POST" and not request.user.is_superuser:  # Allow only non-admin users
        app_id = request.POST.get("app_id")
        app_type = request.POST.get("app_type")

        if app_type == "permission":
            app = get_object_or_404(PermissionApplication, id=app_id, name=request.user.username)
        elif app_type == "leave":
            app = get_object_or_404(LeaveApplication, id=app_id, name=request.user.username)
        else:
            return redirect("requested_forms")  # Invalid type, redirect back

        app.delete()  # Delete only if it belongs to the logged-in user
        return redirect("requested_forms")  # Redirect after deletion

    return redirect("requested_forms")  # Redirect if not allowed





from django.shortcuts import render, redirect, get_object_or_404
from .models import PermissionApplication, LeaveApplication

# Handle updating the status of permission and leave applications
def update_status(request, app_id):
    if request.method == 'POST':
        comment = request.POST.get('comment')  # Get the comment from the form
        app_type = request.POST.get('app_type')  # Determine if it's permission or leave

        if app_type == 'permission':
            # Fetch the PermissionApplication object using the app_id
            app = get_object_or_404(PermissionApplication, id=app_id)
        elif app_type == 'leave':
            # Fetch the LeaveApplication object using the app_id
            app = get_object_or_404(LeaveApplication, id=app_id)
        else:
            # If the app_type is neither 'permission' nor 'leave', we can raise an error
            return redirect('requested_forms')  # Redirect to the requested forms if the app_type is invalid

        # If the app exists, update the status
        app.status = comment
        app.save()

        # After updating, redirect back to the requested forms page
        return redirect('requested_forms')

    # If it's not a POST request, redirect back to the requested forms page
    return redirect('requested_forms')


from django.shortcuts import render
from .models import Employee, Festival

def home(request):
    festivals = Festival.objects.all()  # Fetch all festival data
    birthdays = Employee.objects.all()  # Fetch all employee birthdays

    return render(request, 'home.html', {'festivals': festivals, 'birthdays': birthdays})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Temporary storage for submitted employee data (use a database in production)
employee_data = []

@login_required
def employee_details(request):
    if not request.user.is_staff:  # Check if the user is NOT an admin
        return redirect("details")  # Redirect regular users to details page

    if request.method == "POST":
        name = request.POST.get("name")
        emp_code = request.POST.get("emp_code")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        designation = request.POST.get("designation")
        blood_grp = request.POST.get("blood_grp")
        personal_num = request.POST.get("personal_num")
        official_num = request.POST.get("official_num")
        emergency_num = request.POST.get("emergency_num")
        date_of_join = request.POST.get("date_of_join")
        experience = request.POST.get("experience")
        skill = request.POST.get("skill")
        mail_id = request.POST.get("mail_id")
        adhar_num = request.POST.get("adhar_num")
        pan_num = request.POST.get("pan_num")
        visa = request.POST.get("visa")

        # Store the data with user reference
        employee_data.append({
            "user": request.user.username,  # Associate data with logged-in user
            "name": name,
            "emp_code": emp_code,
            "age": age,
            "gender": gender,
            "address": address,
            "designation": designation,
            "blood_grp": blood_grp,
            "personal_num": personal_num,
            "official_num": official_num,
            "emergency_num": emergency_num,
            "date_of_join": date_of_join,
            "experience": experience,
            "skill": skill,
            "mail_id": mail_id,
            "adhar_num": adhar_num,
            "pan_num": pan_num,
            "visa": visa,
        })

        return redirect("details")  # Redirect to the employee list page

    return render(request, "employee_details.html")


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def details(request):
    # If user is admin (staff), show all employee data
    if request.user.is_staff:
        user_specific_data = employee_data  # Show all employees' data
    else:
        # Regular users should only see their own data where `username` matches `name`
        user_specific_data = [emp for emp in employee_data if emp["name"] == request.user.username]

    return render(request, "details.html", {"employees": user_specific_data})
