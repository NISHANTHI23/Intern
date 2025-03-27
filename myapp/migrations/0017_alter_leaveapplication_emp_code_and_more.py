# Generated by Django 5.1.5 on 2025-03-10 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_leaveapplication_permissionapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveapplication',
            name='emp_code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='leave_on',
            field=models.CharField(choices=[('OD', 'OD'), ('LOP', 'LOP'), ('Others', 'Others')], max_length=20),
        ),
        migrations.AlterField(
            model_name='permissionapplication',
            name='emp_code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='permissionapplication',
            name='permission_on',
            field=models.CharField(choices=[('OD', 'OD'), ('LOP', 'LOP'), ('Others', 'Others')], max_length=20),
        ),
    ]
