# Generated by Django 5.1.5 on 2025-03-10 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_leaveapplication_designation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveapplication',
            name='designation',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='emp_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='leave_on',
            field=models.CharField(choices=[('OD', 'OD (On Duty)'), ('LOP', 'LOP (Loss of Pay)'), ('Others', 'Others')], max_length=50),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='no_of_days',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='permissionapplication',
            name='designation',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='permissionapplication',
            name='emp_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='permissionapplication',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='permissionapplication',
            name='no_of_hours',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='permissionapplication',
            name='permission_on',
            field=models.CharField(choices=[('OD', 'OD (On Duty)'), ('LOP', 'LOP (Loss of Pay)'), ('Others', 'Others')], max_length=50),
        ),
    ]
