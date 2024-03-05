from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Student
from .models import Curfew
from .models import Swipe
from .models import Cq
from .models import Reference
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
    phase_list = [1,2,3]
    return render(request, 'mtlapp/mtl-page/phase_book.html', {'phase_list': phase_list})


def curfew_report(request):
    '''
    '''
    to_return = [s for s in Curfew.objects.all()]
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


def phase1(request):
    '''
    When this function is called it checks all of the students in the database created by the Student model
    to determine their phase. If they are phase 1, then they are passed to the html to be displayed on the phase 1 page.
    The phase 1 html can be found in mtlapp/mtlapp/templates/mtlapp/phase_book/phase1.html. Warren spent hours
    trying to display these because he was stubborn. It's like 5 lines of code XD.
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase == 1:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase1.html', {'students' : to_return})


def phase2(request):
    '''
    When this function is called it checks all of the students in the database created by the Student model
    to determine their phase. If they are phase 2, then they are passed to the html to be displayed on the phase 2 page.
    The phase 2 html can be found in mtlapp/mtlapp/templates/mtlapp/phase_book/phase2.html.
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase == 2:
            to_return.append(s)
            
    return render(request, 'mtlapp/mtl-page/phase_book/phase2.html', {'students' : to_return})


def phase3(request):
    '''
    When this function is called it checks all of the students in the database created by the Student model
    to determine their phase. If they are phase 3, then they are passed to the html to be displayed on the phase 3 page.
    The phase 3 html can be found in mtlapp/mtlapp/templates/mtlapp/phase_book/phase3.html.
    '''
    all_students = [s for s in Student.objects.all()]
    to_return = []
    for s in all_students:
        if s.Phase == 3:
            to_return.append(s)
        
    return render(request, 'mtlapp/mtl-page/phase_book/phase3.html', {'students' : to_return})


def checkinout(request):
    '''
    When this function is called it searches the student database for the student with the matching CAC UUID.
    Once the match has been located, the students check in/out time is updated with the current time
    and their status is set to the opposite of what it was previously. In the case of a valid scan,
    the page is redirected to this same view with an updated list of the 10 most rececent people who scanned.
    In the case of an invalid scan, an almost identical page with an error is redirected to instead.
    This html can be found in mtlapp/mtlapp/templates/mtlapp/checkinout.html.
    '''
    all_students = {s.UUID: s for s in Student.objects.all()}
    to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-35:]
    to_return.reverse()

    today = datetime.datetime.today()
    date = today.weekday()
    now = timezone.localtime()
        
    if request.POST:

        s_uuid = request.POST.get('uuid')
        
        try:
            student = all_students[s_uuid]

        except KeyError:
            return render(request, 'mtlapp/checkinoutbad.html', {'form' : ScanForm, 'students' : to_return})

        student.Checked_In = not student.Checked_In
        student.In_Out_Time = timezone.now()
        student.Time_24_hr = student.In_Out_Time + timezone.timedelta(days=1)
        student.save()
    
        record = Swipe.objects.create(Student=student, In_or_Out=student.Checked_In, Scan_Time=student.In_Out_Time)
        record.save()

        all_students = {s.UUID: s for s in Student.objects.all()}
        to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-35:]
        to_return.reverse()

        if student.Building == '3126 - 312th' and student.Commander_Pass == False and student.Form_4392 == False:

            if student.Phase == 3:
                if ((date == 4 and now < now.replace(hour=3, minute=0, second=0, microsecond=0)) or\
                                                (date == 6 and now > now.replace(hour=22, minute=0, second=0, microsecond=0)) or\
                                                (date < 4 and (now > now.replace(hour=22, minute=0, second=0, microsecond=0) or now < now.replace(hour=3, minute=0, second=0, microsecond=0)))):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()
        
            elif student.Phase == 2:
                if ((date == 4 and now < now.replace(hour=3, minute=0, second=0, microsecond=0)) or\
                                                (date == 6 and now > now.replace(hour=22, minute=0, second=0, microsecond=0)) or\
                                                (date == 5 and now < now.replace(hour=3, minute=0, second=0, microsecond=0)) or\
                                                (date < 4 and (now > now.replace(hour=22, minute=0, second=0, microsecond=0) or now < now.replace(hour=3, minute=0, second=0, microsecond=0)))):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()

            elif student.Phase == 1:
                if (now < now.replace(hour=3, minute=0, second=0, microsecond=0) or now > now.replace(hour=22, minute=0, second=0, microsecond=0)):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()

        all_students = [s for s in Student.objects.all()]
        curfew = [s.Student for s in Curfew.objects.all()]

        for student in all_students:

            if student not in curfew:

                if student.Building == '3126 - 312th' and now > student.Time_24_hr and student.Commander_Pass == False and student.Form_4392 == False:

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Time_24_hr_Broken=True)
                    naughty.save()

        
    return render(request, 'mtlapp/checkinout.html', {'form' : ScanForm, 'students' : to_return})


def checkinoutbad(request):
    '''
    This is the error page that is returned when a CAC UUID scan is invalid. If another invalid scan occurs, the same
    view is requested and if the scan is valid, the user is returned to the error free page.
    This html can be found in mtlapp/mtlapp/templates/mtlapp/checkinoutbad.html. Tsiklauri one shot the inital code
    for this. It instantly worked without any bugs.
    '''
    all_students = {s.UUID: s for s in Student.objects.all()}
    to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-35:]
    to_return.reverse()

    today = datetime.datetime.today()
    date = today.weekday()
    now = timezone.localtime()
        
    if request.POST:

        s_uuid = request.POST.get('uuid')
        
        try:
            student = all_students[s_uuid]

        except KeyError:
            return render(request, 'mtlapp/checkinoutbad.html', {'form' : ScanForm, 'students' : to_return})

        student.Checked_In = not student.Checked_In
        student.In_Out_Time = timezone.now()
        student.Time_24_hr = student.In_Out_Time + timezone.timedelta(days=1)
        student.save()
    
        record = Swipe.objects.create(Student=student, In_or_Out=student.Checked_In, Scan_Time=student.In_Out_Time)
        record.save()

        all_students = {s.UUID: s for s in Student.objects.all()}
        to_return = sorted(all_students.values(), key=lambda x: x.In_Out_Time)[-35:]
        to_return.reverse()


        if student.Building == '3126 - 312th' and student.Commander_Pass == False and student.Form_4392 == False:

            if student.Phase == 3:
                if ((date == 4 and now < now.replace(hour=3, minute=0, second=0, microsecond=0)) or\
                                                (date == 6 and now > now.replace(hour=22, minute=0, second=0, microsecond=0)) or\
                                                (date < 4 and (now > now.replace(hour=22, minute=0, second=0, microsecond=0) or now < now.replace(hour=3, minute=0, second=0, microsecond=0)))):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()     

            elif student.Phase == 2:
                if ((date == 4 and now < now.replace(hour=3, minute=0, second=0, microsecond=0)) or\
                                                (date == 6 and now > now.replace(hour=22, minute=0, second=0, microsecond=0)) or\
                                                (date == 5 and now < now.replace(hour=3, minute=0, second=0, microsecond=0)) or\
                                                (date < 4 and (now > now.replace(hour=22, minute=0, second=0, microsecond=0) or now < now.replace(hour=3, minute=0, second=0, microsecond=0)))):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()

            elif student.Phase == 1:
                if (now < now.replace(hour=3, minute=0, second=0, microsecond=0) or now > now.replace(hour=22, minute=0, second=0, microsecond=0)):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()


        all_students = [s for s in Student.objects.all()]
        curfew = [s.Student for s in Curfew.objects.all()]

        for student in all_students:

            if student not in curfew:

                if student.Building == '3126 - 312th' and now > student.Time_24_hr and student.Commander_Pass == False and student.Form_4392 == False:

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Time_24_hr_Broken=True)
                    naughty.save()

        
        return render(request, 'mtlapp/checkinout.html', {'form' : ScanForm, 'students' : to_return})
        
    return render(request, 'mtlapp/checkinoutbad.html', {'form' : ScanForm, 'students' : to_return})


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
    '''
    if request.POST:
        uuid = request.POST.get('uuid')
        phase = request.POST.get('phase')

        for student in Student.objects.all():
            if uuid == student.UUID:
                student.Phase = phase
                student.save()
                return render(request, 'mtlapp/mtl-page/update_phase.html', {'form' : UpdatePhase})
        
    return render(request, 'mtlapp/mtl-page/update_phase.html', {'form' : UpdatePhase})


def inout(request):
    '''
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
    '''
    cq_duties = [duty.html_display() for duty in Cq.objects.all()]
    return render(request, 'mtlapp/cq_responsibilities.html', {'cq_duties' : cq_duties})

def references(request):
    '''
    '''
    quick_reference = [references.html_display() for references in Reference.objects.all()]
    return render(request, 'mtlapp/references.html', {'quick_reference' : quick_reference})


def swipe_history(request):
    '''
    '''
    all_swipes = [s for s in Swipe.objects.all()]
    to_return = []

    for swipe in all_swipes:
        if swipe.Scan_Time > timezone.now() - timezone.timedelta(days=1):
            to_return.append(swipe)
        
    return render(request, 'mtlapp/mtl-page/swipe_history.html', {'swipes' : to_return})


def auto_curfew():

    today = datetime.datetime.today()
    date = today.weekday()
    now = timezone.localtime()

    all_students = [s for s in Student.objects.all()]

    for student in all_students:

        if student.Checked_In == False and student.Commander_Pass == False and student.Form_4392 == False and student.Building == '3126 - 312th':

            if student.Phase == 3:
                if ((date == 4 and now < now.replace(hour=3, minute=1, second=0, microsecond=0)) or\
                                                (date == 6 and now > now.replace(hour=21, minute=59, second=0, microsecond=0)) or\
                                                (date < 4 and (now > now.replace(hour=21, minute=59, second=0, microsecond=0) or now < now.replace(hour=3, minute=1, second=0, microsecond=0)))):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()     

            elif student.Phase == 2:
                if ((date == 4 and now < now.replace(hour=3, minute=1, second=0, microsecond=0)) or\
                                                (date == 6 and now > now.replace(hour=21, minute=59, second=0, microsecond=0)) or\
                                                (date == 5 and now < now.replace(hour=3, minute=1, second=0, microsecond=0)) or\
                                                (date < 4 and (now > now.replace(hour=21, minute=59, second=0, microsecond=0) or now < now.replace(hour=3, minute=1, second=0, microsecond=0)))):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()

            elif student.Phase == 1:
                if (now < now.replace(hour=3, minute=1, second=0, microsecond=0) or now > now.replace(hour=21, minute=59, second=0, microsecond=0)):

                    naughty = Curfew.objects.create(Student=student, In_or_Out=student.Checked_In, Curfew_Broken=True)
                    naughty.save()
