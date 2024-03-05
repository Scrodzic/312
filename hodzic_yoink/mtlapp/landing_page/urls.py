from django.urls import path
from . import views
from .views import alpha_roster

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('mtl_page', views.mtl_page, name='mtl_page'),
    path('checkinout', views.checkinout, name='checkinout'),
    path('checkinoutbad', views.checkinoutbad, name='checkinoutbad'),
    path('credits', views.credits, name='credits'),
    path('alpha_roster', alpha_roster.as_view(), name='alpha_roster'),
    path('curfew_report', views.curfew_report, name='curfew_report'),
    path('phase_book', views.phase_book, name='phase_book'),
    path('student_notes', views.student_notes, name='student_notes'),
    path('phase1', views.phase1, name='phase1'),
    path('phase2', views.phase2, name='phase2'),
    path('phase3', views.phase3, name='phase3'),
    path('csv_creator', views.csv_creator, name='csv_creator'),
    path('update_phase', views.update_phase, name='update_phase'),
    path('cq_page', views.cq_page, name='cq_page'),
    path('inout', views.inout, name='inout'),
    path('cq_responsibilities', views.cq_responsibilities, name='cq_responsibilities'),
    path('swipe_history', views.swipe_history, name='swipe_history'),
    path('references', views.references, name='references')
]
