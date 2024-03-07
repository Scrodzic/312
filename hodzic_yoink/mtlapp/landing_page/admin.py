from django.contrib import admin
from .models import *
from django.forms import TextInput
from django.db import models

@admin.action(description="Give Commander's pass to selected students")
def give_pass(modeladmin, request, Student):
    Student.update(Commanders_Pass=True)
    
@admin.action(description="Remove Commander's pass from selected students")
def remove_pass(modeladmin, request, Student):
    Student.update(Commanders_Pass=False)
    
@admin.action(description="Add 4392 for selected students")
def give_4392(modeladmin, request, Student):
    Student.update(Form_4392=True)
    
@admin.action(description="Remove 4392 for selected students")
def remove_4392(modeladmin, request, Student):
    Student.update(Form_4392=False)
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    '''
    This class simply sets up navigational features for the admin page that is built into django.
    '''
    list_display = ("Last_Name", "First_Name", "Phase", "Building", "Room", "Specialty")

    list_filter = ("Phase", "Specialty", "Building", "Work_Order", "Form_4392", "Checked_In")

    search_fields = ("Last_Name__startswith", )

    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})}}
    
    actions = [give_pass, remove_pass, give_4392, remove_4392]

    class Meta:
        ordering = ("Last_Name", "First_Name", )


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    '''
    This class simply sets up navigational features for the admin page that is built into django.
    '''
    list_display = ("Student", "Time_of_Occurence", "In_or_Out", "Curfew_Broken", "Time_24_hr_Broken")
    
    list_filter = ("Student", "Time_of_Occurence", "In_or_Out", "Curfew_Broken", "Time_24_hr_Broken")

    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})}}

    class Meta:
        ordering = ("Student.Last_Name", "Student.First_Name", )


@admin.register(Swipe)
class SwipeAdmin(admin.ModelAdmin):
    '''
    '''
    list_display = ("Student", "Scan_Time")

    list_filter = ("Student", "Scan_Time")

    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})}}

    class Meta:
        ordering = ("Student.Last_Name", "Student.First_Name", )


@admin.register(Cq_Duty)
class Cq_DutyAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields = ("Duty_Name__startswith",)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields = ('Reference_Name__startswith',)


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    '''
    '''
    
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    '''
    '''
    list_display = ("Schedule_Name",)
    search_fields = ('Schedule_Name__startswith',)

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields = ('Code__startswith',)
    

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    '''
    '''
    

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields = ('Organization__startswith',)
    

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields = ('Status_Name__startswith',)