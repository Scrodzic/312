import django_tables2 as tables
from .models import Student

class Alpha(tables.Table):
    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap.html"
        fields = ("First_Name", "Last_Name", "Phase", "Building", "Room", "Phone_Number")