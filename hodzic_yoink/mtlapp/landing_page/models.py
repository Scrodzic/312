from django.db import models
from django.utils import timezone
import datetime as dt

class Student(models.Model):
    '''
    A model class that initializes a student in a sqlite database.
    '''
    UUID = models.CharField(max_length=25, default='Please Enter CAC UUID')
    First_Name = models.CharField(max_length=25)
    Last_Name = models.CharField(max_length=25)
    Gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female')])
    Specialty = models.ForeignKey(Specialty)
    Rank = models.ForeignKey(Rank)
    Service = models.CharField(max_length=10, choices=[('USAF', 'USAF'), ('ARMY', 'ARMY'), ('USN', 'USN'), ('USMC', 'USMC'), ('USCG', 'USCG'), ('USSF', 'USSF'), ('Civilian', 'Civilian'), ('Other', 'Other')])
    Active_Status = models.CharField(max_length=20, choices=[('Active Duty', 'Active Duty'), ('Guard', 'Guard'), ('Reserve', 'Reserve'), ('N/A', 'N/A')])
    Notes = models.TextField(blank=True, null=True)
    Phone_Number = models.CharField(max_length=20)
    Email = models.CharField(max_length=50, blank=True, null=True)
    Date_of_Arrival = models.DateField(default=dt.date.today() - dt.timedelta(days=1))
    Building = models.ForeignKey(Building)
    Room = models.IntegerField()
    Work_Order = models.BooleanField(default=False)
    Work_Order_Note = models.TextField(blank=True, null=True)
    Phase = models.ForeignKey(Phase)
    Status = models.ForeignKey(Status)
    Commanders_Pass = models.BooleanField(default=False)
    Form_4392 = models.BooleanField(default=False)
    Checked_In = models.BooleanField(default=False)
    In_Out_Time = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    Time_24_hr = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1), blank=True, null=True)

    
    def csv(self):
        return f'{self.UUID}, {self.First_Name}, {self.Last_Name}, {self.Gender}, {self.Specialty}, {self.Rank}, {self.Service}, {self.Active_Status}, {self.Notes}, {self.Phone_Number}, {self.Email}, {self.Date_of_Arrival}, {self.Building}, {self.Room}, {self.Work_Order}, {self.Work_Order_Note}, {self.Phase}, {self.Status}'

    def __str__(self):
        return f'{self.Last_Name}, {self.First_Name}'


class Curfew(models.Model):
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


class Cq(models.Model):
    '''
    '''
    Duty_Name = models.CharField(max_length=25)
    Duties = models.TextField()

    def __str__(self):
        return f'{self.Duty_Name}'

    def html_display(self):
        return f'{self.Duties}'


class Reference(models.Model):
    '''
    '''
    Reference_Name = models.CharField(max_length=25)
    Quick_Reference = models.TextField()

    def __str__(self):
        return f'{self.Reference_Name}'

    def html_display(self):
        return f'{self.Quick_Reference}'


class Phase(models.Model):
    '''
    '''
    Number = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])
    Prior_Duty_Day_Curfew_From = models.TimeField(blank=True, null=True)
    Prior_Duty_Day_Curfew_To = models.TimeField(blank=True, null=True)
    Prior_Non_Duty_Day_Curfew_From = models.TimeField(blank=True, null=True)
    Prior_Non_Duty_Day_Curfew_To = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.Number}'
    
    
class Specialty(models.Model):
    '''
    '''
    Code = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.Code}'
    

class Rank(models.Model):
    '''
    '''
    Type = models.CharField(choices=[('Enlisted', 'Officer', 'Civilian', 'Other')])
    Grade = models.CharField(choices=[('N/A', 'N/A'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])
    Name = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.Type}, {self.Grade}, {self.Name}'
    
    
class Building(models.Model):
    '''
    '''
    Organization = models.CharField(max_length=20)
    Number = models.CharField(max_length=10)
    Address = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f'{self.Organization}, {self.Number}'

    
class Status(models.Model):
    '''
    '''
    Status_Name = models.CharField(max_length=20)
    Description = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.Status_Name}'