from django.contrib import admin
from .models import Course, Lesson, Instructor, Enrollment, Question, Choice, Submission


# ChoiceInline - Task 2
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


# QuestionInline - Task 2
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


# QuestionAdmin - Task 2
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']
    search_fields = ['content']


# LessonAdmin - Task 2
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course', 'order']
    search_fields = ['title']


# CourseAdmin with LessonInline
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['name', 'pub_date']
    search_fields = ['name', 'description']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
