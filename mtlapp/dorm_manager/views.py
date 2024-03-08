from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import Alpha
from .forms import ScanForm
from .forms import UpdatePhase
from .forms import StudentSearch
import datetime as dt
from django.utils import timezone
from datetime import date
import datetime
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Half of the imports in this project aren't even used btw but I think its better to accidentally import everything
# than looking for that one module you forgot to import.

# The views are the heart of a django project, they are what 'speak' with the data and the webpage that displays it.
# The views will recieve a request when a url from urls.py is requested by a browser. The view will then typicaly
# render an html that the user can interact with. Knowing how all of these modules interact with eachother is crucial
# to understanding and creating a robust django project.
# All of the following views have an argument called 'request' because they are called by url request.
# If adding your own html, make sure it is located somewhere within the mtlapp/mtlapp/templates/mtlapp directory,
# and that the file path is properly referenced and that the mtlapp/mtlapp/landing_page/urls.py properly references
# the url address and html that you wish it to.
# If using git, make sure you don't have some goober causing havoc upstream from everyone else.
class alpha_roster(SingleTableView):
    '''
    This class references a table created by django tables 2 and creates a table object which is rendered in the html.
    '''
    model = Student
    table_class = Alpha
    template_name = 'mtlapp/mtl-page/alpha_roster.html'


def landing_page(request):
    '''
    When this function is called, it simply returns a render of the landing page html.
    The landing page is the default url when launching the server
    and can be found in mtlapp/mtlapp/templates/mtlapp/landing_page.html.
    '''
    return render(request, 'mtlapp/landing_page.html')

@staff_member_required
def mtl_page(request):
    '''
    When this function is called, it simply returns a render of the mtl home page html.
    The mtl home page contains navigation to mtl resources
    and can be found in mtlapp/mtlapp/templates/mtlapp/mtl_page.html.
    The staff_member_required decorator makes the page password protected.
    This can be configured in the mtlapp/mtlapp/settings.py
    '''
    return render(request, 'mtlapp/mtl_page.html')


def admin(request):
    '''
    When this function is called, it simply returns a render of the admin page.
    The admin page contains the ability to add, update, and remove students in the system
    and can be found and configured in mtlapp/landing_page/admin.py.
    '''
    return render(request, 'mtlapp/admin.html')


def credits(request):
    '''
    When this function is called, it simply returns a render of the credits page html.
    The credits page is a neat little page created by the greatest red rope to ever walk the Earth
    and can be found in mtlapp/mtlapp/templates/mtlapp/credits.html.
    '''
    return render(request, 'mtlapp/credits.html')

def phase_book(request):
    '''
    When this function is called, it simply returns a render of the phase book page html.
    It also passes a list of phases which are looped through in the html to create identical buttons.
    The phase book is simply a navigational page to view a table of every student in each phase
    and can be found in mtlapp/mtlapp/templates/mtlapp/mtl_page/phase_book.html.
    '''
    phase_list = sorted(['phase' + str(x.Number) for x in Phase.objects.all()])
    
    return render(request, 'mtlapp/mtl-page/phase_book.html', {'phase_list': phase_list})


def curfew_report(request):
    '''
    When this function is called, it returns 2 lists of all of the objects in the violation table.
    The tables are rendered on the curfew report html which can be found in 
    mtlapp/mtlapp/templates/mtlapp/mtl-page/curfew_report.html.
    '''
    to_return = [s for s in Violation.objects.all()]
    curfew = []
    twenty_four = []

    for student in to_return:
        if student.Curfew_Broken == True:
            curfew.append(student)

        else:
            twenty_four.append(student)
    
    return render(request, 'mtlapp/mtl-page/curfew_report.html', {'curfew': curfew, 'twenty_four': twenty_four})


def student_notes(request):
    '''
    When this function is called it checks all of the students in the database created by the Student model
    to determine if they have a note in the system. If they have a note,
    then they are passed to the html to be displayed on the student notes page.
    The student notes html can be found in mtlapp/mtlapp/templates/mtlapp/student_notes.html.
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Notes != '':
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/student_notes.html', {'students': to_return})


def checkinout(request):
    '''
    When this function is called it searches the student database for the student with the matching CAC UUID.
    Once the match has been located, the students check in/out time is updated with the current time
    and their status is set to the opposite of what it was previously. In the case of a valid scan,
    the page is redirected to this same view with an updated list of the 30 most rececent people who scanned.
    In the case of an invalid scan, an almost identical page with an error is redirected to instead.
    This request also checks if the student who scanned is past their curfew and logs the scan in the violation table
    if true. This request also checks if any student in the database hasn't scanned in the past 24 hours and also
    logs them once in the violation table.
    This html can be found in mtlapp/mtlapp/templates/mtlapp/checkinout.html.
    '''
    all_students = {s.UUID: s for s in Student.objects.all()}
    to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-30:]
    to_return.reverse()
    
    banner = [message.html_display() for message in Banner.objects.all()]

    today = datetime.datetime.today()
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    date = today.weekday()
    tomorrow_date = tomorrow.weekday()
    now = timezone.localtime()
    now_time = now.time()
        
    if request.POST:

        s_uuid = request.POST.get('uuid')
        
        try:
            student = all_students[s_uuid]

        except KeyError:
            return render(request, 'mtlapp/checkinoutbad.html', {'form' : ScanForm, 'students' : to_return, 'banner': banner})

        student.Checked_In = not student.Checked_In
        student.In_Out_Time = timezone.now()
        student.Time_24_hr = student.In_Out_Time + timezone.timedelta(days=1)
        student.save()
    
        record = Swipe.objects.create(Student=student, In_or_Out=student.Checked_In, Scan_Time=student.In_Out_Time)
        record.save()

        all_students = {s.UUID: s for s in Student.objects.all()}
        to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-30:]
        to_return.reverse()

        if student.Building.Curfew_Applies == True and student.Commanders_Pass == False and student.Form_4392 == False:

            schedule = [student.Schedule.Monday, student.Schedule.Tuesday, student.Schedule.Wednesday, student.Schedule.Thursday,\
                        student.Schedule.Friday, student.Schedule.Saturday, student.Schedule.Sunday]
        
            if student.Checked_In == False and student.Commanders_Pass == False and student.Form_4392 == False and student.Building.Curfew_Applies == True:

                if ((schedule[date] == 'Duty Day' and schedule[tomorrow_date] == 'Non Duty Day' and now_time < student.Phase.Duty_Day_Curfew_To) or\
                                                (schedule[date] == 'Non Duty Day' and schedule[tomorrow_date] == 'Duty Day' and now_time > student.Phase.Duty_Day_Curfew_From) or\
                                                (schedule[date] == 'Non Duty Day' and schedule[tomorrow_date] == 'Non Duty Day' and (now_time > student.Phase.Non_Duty_Day_Curfew_From or now_time < student.Phase.Non_Duty_Day_Curfew_To)) or\
                                                (schedule[date] =='Duty Day' and schedule[tomorrow_date] == 'Duty Day' and (now_time > student.Phase.Duty_Day_Curfew_From or now_time < student.Phase.Duty_Day_Curfew_To))):

                    naughty = Violation.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()


        all_students = [s for s in Student.objects.all()]
        curfew = [s.Student for s in Violation.objects.all()]

        for student in all_students:

            if student not in curfew:

                if student.Building.Curfew_Applies == True and now > student.Time_24_hr and student.Commanders_Pass == False and student.Form_4392 == False:

                    naughty = Violation.objects.create(Student=student, In_or_Out=student.Checked_In, Time_24_hr_Broken=True)
                    naughty.save()

        
    return render(request, 'mtlapp/checkinout.html', {'form' : ScanForm, 'students' : to_return, 'banner': banner})


def checkinoutbad(request):
    '''
    This is the error page that is returned when a CAC UUID scan is invalid. If another invalid scan occurs, the same
    view is requested and if the scan is valid, the user is returned to the error free page.
    This html can be found in mtlapp/mtlapp/templates/mtlapp/checkinoutbad.html. Tsiklauri one shot the inital code
    for this. It instantly worked without any bugs.
    '''
    all_students = {s.UUID: s for s in Student.objects.all()}
    to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-30:]
    to_return.reverse()
    
    banner = [message.html_display() for message in Banner.objects.all()]

    today = datetime.datetime.today()
    tomorrow = datetime.datime.today() + datetime.timedelta(days=1)
    date = today.weekday()
    tomorrow_date = tomorrow.weekday()
    now = timezone.localtime()
    now_time = now.time()
        
    if request.POST:

        s_uuid = request.POST.get('uuid')
        
        try:
            student = all_students[s_uuid]

        except KeyError:
            return render(request, 'mtlapp/checkinoutbad.html', {'form' : ScanForm, 'students' : to_return, 'banner': banner})

        student.Checked_In = not student.Checked_In
        student.In_Out_Time = timezone.now()
        student.Time_24_hr = student.In_Out_Time + timezone.timedelta(days=1)
        student.save()
    
        record = Swipe.objects.create(Student=student, In_or_Out=student.Checked_In, Scan_Time=student.In_Out_Time)
        record.save()

        all_students = {s.UUID: s for s in Student.objects.all()}
        to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-30:]
        to_return.reverse()

        if student.Building.Curfew_Applies == True and student.Commanders_Pass == False and student.Form_4392 == False:

            schedule = [student.Schedule.Monday, student.Schedule.Tuesday, student.Schedule.Wednesday, student.Schedule.Thursday,\
                        student.Schedule.Friday, student.Schedule.Saturday, student.Schedule.Sunday]
        
            if student.Checked_In == False and student.Commanders_Pass == False and student.Form_4392 == False and student.Building.Curfew_Applies == True:

                if ((schedule[date] == 'Duty Day' and schedule[tomorrow_date] == 'Non Duty Day' and now_time < student.Phase.Duty_Day_Curfew_To) or\
                                                (schedule[date] == 'Non Duty Day' and schedule[tomorrow_date] == 'Duty Day' and now_time > student.Phase.Duty_Day_Curfew_From) or\
                                                (schedule[date] == 'Non Duty Day' and schedule[tomorrow_date] == 'Non Duty Day' and (now_time > student.Phase.Non_Duty_Day_Curfew_From or now_time < student.Phase.Non_Duty_Day_Curfew_To)) or\
                                                (schedule[date] =='Duty Day' and schedule[tomorrow_date] == 'Duty Day' and (now_time > student.Phase.Duty_Day_Curfew_From or now_time < student.Phase.Duty_Day_Curfew_To))):

                    naughty = Violation.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()


        all_students = [s for s in Student.objects.all()]
        curfew = [s.Student for s in Violation.objects.all()]

        for student in all_students:

            if student not in curfew:

                if student.Building.Number == '3126' and now > student.Time_24_hr and student.Commanders_Pass == False and student.Form_4392 == False:

                    naughty = Violation.objects.create(Student=student, In_or_Out=student.Checked_In, Time_24_hr_Broken=True)
                    naughty.save()

        
        return render(request, 'mtlapp/checkinout.html', {'form' : ScanForm, 'students' : to_return, 'banner': banner})
        
    return render(request, 'mtlapp/checkinoutbad.html', {'form' : ScanForm, 'students' : to_return, 'banner': banner})


def csv_creator(request):
    '''
    When this function is called, a csv is created named, "squadron_data.csv." The csv is populated
    with the features pulled from the Student model method "csv".
    '''
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="squadron_data.csv"'},
    )

    writer = csv.writer(response)
    for student in Student.objects.all():
        student = student.csv().split(', ')
        writer.writerow(student)

    return response


def update_phase(request):
    '''
    This function contains a form that accepts an input of the available phases and a student's UUID.
    When the form is submitted, it updates the student's phase with the one selected.
    The html can be located in mtlapp/mtlapp/mtl-page/update_phase.html.
    '''
    if request.POST:
        uuid = request.POST.get('uuid')
        phase = request.POST.get('phase')

        for student in Student.objects.all():
            if uuid == student.UUID:
                student.Phase.Number = phase
                student.save()
                return render(request, 'mtlapp/mtl-page/update_phase.html', {'form' : UpdatePhase})
        
    return render(request, 'mtlapp/mtl-page/update_phase.html', {'form' : UpdatePhase})


def inout(request):
    '''
    This function contains a form that accepts an input of a student's last name
    When the form is submitted, it returns a render of a table containing some basic information of the student.
    This is meant for simply searching for a student and locating them based on their in or out status.
    This html can be located in mtlapp/mtlapp/templates/mtlapp/inout.html.
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []

    if request.POST:
        lname = request.POST.get('Last_Name')

        for student in all_students:
            if lname.lower() == student.Last_Name.lower():
                to_return.append(student)
               
        return render(request, 'mtlapp/inout.html', {'form' : StudentSearch,'students' : to_return})
        
    return render(request, 'mtlapp/inout.html', {'form' : StudentSearch,'students' : to_return})


def cq_page(request):
    '''
    When this function is called, it simply returns a render of the cq home page html.
    The cq home page contains navigation to cq resources
    and can be found in mtlapp/mtlapp/templates/mtlapp/cq_page.html.
    '''
    return render(request, 'mtlapp/cq_page.html')


def cq_responsibilities(request):
    '''
    This function returns all of the objects contained in the cq_duty table.
    The html rendered displays the CQ responsibilities so that CQ personnel may
    keep up to date with their required duties. This html may be located in
    mltapp/mtlapp/templates/mtlapp/cq_responsibilities.html.
    '''
    cq_duties = [duty.html_display() for duty in Cq_Duty.objects.all()]
    return render(request, 'mtlapp/cq_responsibilities.html', {'cq_duties' : cq_duties})

def references(request):
    '''
    Similarly to the cq_responsibilities function, this function returns all of the objects contained in the references table.
    The html rendered displays all of the CQ quick references so that CQ personnel may
    have quick access to pertinent information. This html may be located in
    mltapp/mtlapp/templates/mtlapp/references.html.
    '''
    quick_reference = [references.html_display() for references in Reference.objects.all()]
    return render(request, 'mtlapp/references.html', {'quick_reference' : quick_reference})


def swipe_history(request):
    '''
    This function returns all of the scans in the swipe history table and
    returns a rendering of an html that displays every scan in the past day.
    All scans are still visible through the admin page. This html may be located in
    mltapp/mtlapp/templates/mtlapp/mtl-page/swipe_history.html.
    '''
    all_swipes = [s for s in Swipe.objects.all()]
    to_return = []

    for swipe in all_swipes:
        if swipe.Scan_Time > timezone.now() - timezone.timedelta(days=1):
            to_return.append(swipe)
        
    return render(request, 'mtlapp/mtl-page/swipe_history.html', {'swipes' : to_return})


def auto_curfew():
    '''
    This function checks all of the student objects to see if on is out past curfew.
    This is necessary in addition to the check that happens when someone scans because
    if a student is out before curfew and returns after curfew, they will not be picked up.
    This function will run based on a crontab cronjob. This can be configured in the settings.py.
    '''
    today = datetime.datetime.today()
    tomorrow = datetime.datime.today() + datetime.timedelta(days=1)
    date = today.weekday()
    tomorrow_date = tomorrow.weekday()
    now = timezone.localtime()
    now = now.time()

    all_students = [s for s in Student.objects.all()]

    for student in all_students:

        schedule = [student.Schedule.Monday, student.Schedule.Tuesday, student.Schedule.Wednesday, student.Schedule.Thursday,\
                    student.Schedule.Friday, student.Schedule.Saturday, student.Schedule.Sunday]
        
        if student.Checked_In == False and student.Commanders_Pass == False and student.Form_4392 == False and student.Building.Curfew_Applies == True:

            if ((schedule[date] == 'Duty Day' and schedule[tomorrow_date] == 'Non Duty Day' and now < student.Phase.Duty_Day_Curfew_To) or\
                                            (schedule[date] == 'Non Duty Day' and schedule[tomorrow_date] == 'Duty Day' and now > student.Phase.Duty_Day_Curfew_From) or\
                                            (schedule[date] == 'Non Duty Day' and schedule[tomorrow_date] == 'Non Duty Day' and (now > student.Phase._Non_Duty_Day_Curfew_From or now < student.Phase.Non_Duty_Day_Curfew_To)) or\
                                            (schedule[date] =='Duty Day' and schedule[tomorrow_date] == 'Duty Day' and (now > student.Phase.Duty_Day_Curfew_From or now < student.Phase.Duty_Day_Curfew_To))):

                naughty = Violation.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                naughty.save()
                
                
def phase0(request):
    '''
    When this function is called it checks all of the students in the database created by the Student model
    to determine their phase. If they are phase 1, then they are passed to the html to be displayed on the phase 1 page.
    The phase 1 html can be found in mtlapp/mtlapp/templates/mtlapp/phase_book/phase1.html. Warren spent hours
    trying to display these because he was stubborn. It's like 5 lines of code XD.
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 0:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase0.html', {'students' : to_return})


def phase1(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 1:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase1.html', {'students' : to_return})


def phase2(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 2:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase2.html', {'students' : to_return})


def phase3(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 3:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase3.html', {'students' : to_return})


def phase4(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 4:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase4.html', {'students' : to_return})


def phase5(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 5:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase5.html', {'students' : to_return})


def phase6(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 6:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase6.html', {'students' : to_return})


def phase7(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 7:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase7.html', {'students' : to_return})


def phase8(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 8:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase8.html', {'students' : to_return})


def phase9(request):
    '''
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase.Number == 9:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase9.html', {'students' : to_return})