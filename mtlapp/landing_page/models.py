from django.db import models
from django.utils import timezone
import datetime as dt

class Phase(models.Model):
    '''
    '''
    Number = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])
    Duty_Day_Curfew_From = models.TimeField(blank=True, null=True)
    Duty_Day_Curfew_To = models.TimeField(blank=True, null=True)
    Non_Duty_Day_Curfew_From = models.TimeField(blank=True, null=True)
    Non_Duty_Day_Curfew_To = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.Number}'
    

class Schedule(models.Model):
    '''
    '''
    Schedule_Name = models.CharField(max_length=20)
    Monday = models.CharField(max_length=15, choices=[('Duty Day', 'Duty Day'), ('Non Duty Day', 'Non Duty Day')])
    Tuesday = models.CharField(max_length=15, choices=[('Duty Day', 'Duty Day'), ('Non Duty Day', 'Non Duty Day')])
    Wednesday = models.CharField(max_length=15, choices=[('Duty Day', 'Duty Day'), ('Non Duty Day', 'Non Duty Day')])
    Thursday = models.CharField(max_length=15, choices=[('Duty Day', 'Duty Day'), ('Non Duty Day', 'Non Duty Day')])
    Friday = models.CharField(max_length=15, choices=[('Duty Day', 'Duty Day'), ('Non Duty Day', 'Non Duty Day')])
    Saturday = models.CharField(max_length=15, choices=[('Duty Day', 'Duty Day'), ('Non Duty Day', 'Non Duty Day')])
    Sunday = models.CharField(max_length=15, choices=[('Duty Day', 'Duty Day'), ('Non Duty Day', 'Non Duty Day')])
    
    def __str__(self):
        return f'{self.Schedule_Name}'
    
    
class Specialty(models.Model):
    '''
    '''
    Code = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.Code}'
    
    class Meta:
        verbose_name_plural = "Specialties"
    

class Rank(models.Model):
    '''
    '''
    Type = models.CharField(max_length=15, choices=[('E', 'E'), ('O', 'O'), ('Civilian', 'Civilian'), ('Other', 'Other')])
    Grade = models.CharField(max_length=5, choices=[('N/A', 'N/A'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')])
    Rank_Name = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.Type}, {self.Grade}, {self.Rank_Name}'
    
    
class Building(models.Model):
    '''
    '''
    Organization = models.CharField(max_length=20)
    Number = models.CharField(max_length=10)
    Address = models.CharField(max_length=50, blank=True, null=True)
    Curfew_Applies = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.Organization}, {self.Number}'

    
class Status(models.Model):
    '''
    '''
    Status_Name = models.CharField(max_length=20)
    Description = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.Status_Name}'
    
    class Meta:
        verbose_name_plural = "Status'"
    

class Student(models.Model):
    '''
    A model class that initializes a student in a sqlite database.
    '''
    UUID = models.CharField(max_length=25, default='Please Enter CAC UUID')
    First_Name = models.CharField(max_length=25)
    Last_Name = models.CharField(max_length=25)
    Gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female')])
    Specialty = models.ForeignKey(Specialty, null=True, on_delete=models.SET_NULL)
    Rank = models.ForeignKey(Rank, null=True, on_delete=models.SET_NULL)
    Service = models.CharField(max_length=10, choices=[('USAF', 'USAF'), ('ARMY', 'ARMY'), ('USN', 'USN'), ('USMC', 'USMC'), ('USCG', 'USCG'), ('USSF', 'USSF'), ('Civilian', 'Civilian'), ('Other', 'Other')])
    Active_Status = models.CharField(max_length=20, choices=[('Active Duty', 'Active Duty'), ('Guard', 'Guard'), ('Reserve', 'Reserve'), ('N/A', 'N/A')])
    Notes = models.TextField(blank=True, null=True)
    Phone_Number = models.CharField(max_length=20)
    Email = models.CharField(max_length=50, blank=True, null=True)
    Date_of_Arrival = models.DateField(default=dt.date.today() - dt.timedelta(days=1))
    Building = models.ForeignKey(Building, null=True, on_delete=models.SET_NULL)
    Room = models.IntegerField()
    Work_Order = models.BooleanField(default=False)
    Work_Order_Note = models.TextField(blank=True, null=True)
    Phase = models.ForeignKey(Phase, null=True, on_delete=models.SET_NULL)
    Status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)
    Schedule = models.ForeignKey(Schedule, null=True, on_delete=models.SET_NULL)
    Commanders_Pass = models.BooleanField(default=False)
    Form_4392 = models.BooleanField(default=False)
    Checked_In = models.BooleanField(default=False)
    In_Out_Time = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    Time_24_hr = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1), blank=True, null=True)
    
    def csv(self):
        return f'{self.UUID}, {self.First_Name}, {self.Last_Name}, {self.Gender}, {self.Specialty}, {self.Rank}, {self.Service}, {self.Active_Status}, {self.Notes}, {self.Phone_Number}, {self.Email}, {self.Date_of_Arrival}, {self.Building}, {self.Room}, {self.Work_Order}, {self.Work_Order_Note}, {self.Phase}, {self.Status}'

    def __str__(self):
        return f'{self.Last_Name}, {self.First_Name}'


class Violation(models.Model):
    '''
    '''
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Time_of_Occurence = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    In_or_Out = models.BooleanField(default=False)
    Curfew_Broken = models.BooleanField(default=False)
    Time_24_hr_Broken = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.Student.Last_Name}, {self.Student.First_Name}'


class Swipe(models.Model):
    '''
    '''
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Scan_Time = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    In_or_Out = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Student.Last_Name}, {self.Student.First_Name}'


class Cq_Duty(models.Model):
    '''
    '''
    Duty_Name = models.CharField(max_length=25)
    Duties = models.TextField()

    def __str__(self):
        return f'{self.Duty_Name}'

    def html_display(self):
        return f'{self.Duties}'
    
    class Meta:
        verbose_name_plural = "CQ Duties"


class Reference(models.Model):
    '''
    '''
    Reference_Name = models.CharField(max_length=25)
    Quick_Reference = models.TextField()

    def __str__(self):
        return f'{self.Reference_Name}'

    def html_display(self):
        return f'{self.Quick_Reference}'