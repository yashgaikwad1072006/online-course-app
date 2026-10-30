from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Course, Enrollment, Question, Choice, Submission


# Registration view
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except Exception:
            pass
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


# Login view
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


# Logout view
def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


# Check enrollment helper
def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        try:
            Enrollment.objects.get(user=user, course=course)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass
    return is_enrolled


# Course list view
class CourseListView(generic.ListView):
    model = Course
    template_name = 'onlinecourse/course_list_bootstrap.html'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


# Course detail view
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'


# Enroll view
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        enrollment = Enrollment.objects.create(
            user=user,
            course=course,
            mode='honor'
        )
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(
        reverse(viewname='onlinecourse:course_details', args=(course.id,))
    )


# Submit exam view - Task 5
def submit(request, course_id):
    """
    Handles exam submission. Retrieves the current user's enrollment,
    creates a new Submission, and records all selected choices.
    """
    user = request.user
    course = get_object_or_404(Course, pk=course_id)

    # Get the enrollment for this user and course
    try:
        enrollment = Enrollment.objects.get(user=user, course=course)
    except Enrollment.DoesNotExist:
        return redirect('onlinecourse:index')

    # Create a new submission linked to this enrollment
    submission = Submission.objects.create(enrollment=enrollment)

    # Collect all selected choice IDs from the submitted form
    submitted_answers = []
    for key, value in request.POST.items():
        if key.startswith('choice'):
            choice_id = int(value)
            submitted_answers.append(choice_id)
            try:
                selected_choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(selected_choice)
            except Choice.DoesNotExist:
                pass

    submission.save()

    return HttpResponseRedirect(
        reverse(
            viewname='onlinecourse:show_exam_result',
            args=(course_id, submission.id)
        )
    )


# Show exam result view - Task 5
def show_exam_result(request, course_id, submission_id):
    """
    Retrieves the submission, evaluates each question,
    calculates the total score, and renders the result template.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Get the IDs of all selected choices in this submission
    selected_ids = submission.choices.values_list('id', flat=True)

    # Get all questions for this course
    questions = Question.objects.filter(course=course)

    total_score = 0
    question_results = []

    for question in questions:
        is_correct = question.is_get_score(selected_ids)
        if is_correct:
            total_score += question.grade

        question_results.append({
            'question': question,
            'is_correct': is_correct,
            'selected_choices': question.choice_set.filter(id__in=selected_ids),
        })

    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'question_results': question_results,
        'pass_score': 80,
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
