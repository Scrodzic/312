# Generated by Django 4.2.10 on 2024-03-07 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0002_alter_student_in_out_time_alter_student_time_24_hr_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phase',
            old_name='Prior_Duty_Day_Curfew_From',
            new_name='Duty_Day_Curfew_From',
        ),
        migrations.RenameField(
            model_name='phase',
            old_name='Prior_Duty_Day_Curfew_To',
            new_name='Duty_Day_Curfew_To',
        ),
        migrations.RenameField(
            model_name='phase',
            old_name='Prior_Non_Duty_Day_Curfew_From',
            new_name='Non_Duty_Day_Curfew_From',
        ),
        migrations.RenameField(
            model_name='phase',
            old_name='Prior_Non_Duty_Day_Curfew_To',
            new_name='Non_Duty_Day_Curfew_To',
        ),
        migrations.AlterField(
            model_name='student',
            name='In_Out_Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 7, 14, 25, 5, 44222, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='Time_24_hr',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 8, 14, 25, 5, 44286, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='swipe',
            name='Scan_Time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 7, 14, 25, 5, 48432, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='violation',
            name='Time_of_Occurence',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 7, 14, 25, 5, 47045, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
