from django.contrib import admin
import models
from django.forms import TextInput
from django.db import models

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    '''
    This class simply sets up navigational features for the admin page that is built into django.
    '''
    list_display = ("Last_Name", "First_Name", "Phase", "Building", "Room", "AFSC")

    list_filter = ("Phase", "AFSC", "Building", "Work_Order", "Form_4392", "Checked_In")

    search_fields = ("Last_Name__startswith", )

    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})}}

    class Meta:
        ordering = ("Last_Name", "First_Name", )


@admin.register(Curfew)
class CurfewAdmin(admin.ModelAdmin):
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


@admin.register(Cq)
class CqAdmin(admin.ModelAdmin):
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