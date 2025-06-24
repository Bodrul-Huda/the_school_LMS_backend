
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import MarkLessonCompletedAPIView, activate_enrolment, category_list_create, create_checkout_session, material_list_create, enrolment_list_create, course_detail, lesson_list_create, questionAnswer_list_create, course_list_create

urlpatterns = [
    path('categories/', category_list_create, name='category_list_create'),
    path('courses/', course_list_create, name='course_list_create'),
    path('materials/', material_list_create, name='material_list_create'),
    path('enrolment/', enrolment_list_create, name='enrolment_list_create'),
    path('details/<int:pk>/', course_detail, name='course_detail'),
    path('lesson/', lesson_list_create, name='lesson_list_create'),
    path('question/', questionAnswer_list_create, name='questionAnswer_list_create'),
    path('lessons/complete/', MarkLessonCompletedAPIView.as_view(), name='mark-lesson-complete'),
    path('create-checkout-session/', create_checkout_session),
    path('enrol/activate/', activate_enrolment, name='activate_enrolment'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)