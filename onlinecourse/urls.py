from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Course list (home)
    path(route='', view=views.CourseListView.as_view(), name='index'),

    # User registration, login, logout
    path(route='registration/', view=views.registration_request, name='registration'),
    path(route='login/', view=views.login_request, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),

    # Course detail
    path(route='course/<int:pk>/', view=views.CourseDetailView.as_view(), name='course_details'),

    # Enroll
    path(route='enroll/<int:course_id>/', view=views.enroll, name='enroll'),

    # Submit exam - Task 6
    path(route='course/<int:course_id>/submit/', view=views.submit, name='submit'),

    # Show exam result - Task 6
    path(
        route='course/<int:course_id>/submission/<int:submission_id>/result/',
        view=views.show_exam_result,
        name='show_exam_result'
    ),
]
