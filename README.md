# Django Online Course Application

A Django-based Online Course application with exam/assessment features.

## Features

- Course listing and detail views
- User registration, login, and logout
- Course enrollment
- Exam questions with multiple-choice answers
- Exam submission and result evaluation

## Setup

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Project Structure

- `onlinecourse/models.py` — Course, Lesson, Instructor, Enrollment, Question, Choice, Submission
- `onlinecourse/admin.py` — Admin configuration with inlines
- `onlinecourse/views.py` — All views including submit and show_exam_result
- `onlinecourse/urls.py` — URL routing including exam paths
- `onlinecourse/templates/` — Bootstrap-styled HTML templates
