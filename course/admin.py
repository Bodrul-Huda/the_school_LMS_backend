from django.contrib import admin
from .models import Category, Course, Material, Lesson, QuestionAnswer, Enrolment

# Register your models here.

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Material)
admin.site.register(Lesson)
admin.site.register(QuestionAnswer)
admin.site.register(Enrolment)
