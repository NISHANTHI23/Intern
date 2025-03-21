from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('Admin', 'Admin'), ('User', 'User')], default='User')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Festival(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.name



class Festival(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name


class RelievingRule(models.Model):
    file = models.FileField(upload_to='relieving_rules/')
    
    def __str__(self):
        return f"Rule {self.id}"





from django.db import models

class OfferLetter(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    offer_letter = models.FileField(upload_to='offer_letters/')

    def __str__(self):
        return self.name


# models.py
# models.py

from django.db import models

class Rule(models.Model):
    rule = models.TextField(blank=True, null=True)  # For storing text-based rules
    file = models.FileField(upload_to='office_criteria/', null=True, blank=True)  # For file uploads

    def __str__(self):
        return self.rule if self.rule else str(self.file)



class RelievingRule(models.Model):
    file = models.FileField(upload_to='relieving_rules/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # Only this

    def __str__(self):
        return f"Rule uploaded on {self.created_at}"


class TeamMember(models.Model):
    team_name = models.CharField(max_length=100)
    member_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.member_name} - {self.team_name}"


class TimeEntry(models.Model):
    member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name="time_entries")
    time_in = models.DateTimeField()  # Store each time-in entry

    def __str__(self):
        return f"{self.member.member_name} - {self.time_in}"


from django.db import models

class PermissionApplication(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=100)
    permission_from = models.TimeField()
    permission_till = models.TimeField()
    no_of_hours = models.IntegerField()
    purpose = models.TextField()
    permission_on = models.CharField(max_length=100)
    status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Permission Application by {self.name}"

class LeaveApplication(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=100)
    leave_from = models.DateField()
    leave_till = models.DateField()
    no_of_days = models.IntegerField()
    purpose = models.TextField()
    leave_on = models.CharField(max_length=100)
    status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Leave Application by {self.name}"




