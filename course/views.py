from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from course.serializers import CategorySerializer, CourseSerializer, EnrolmentSerializer, LessonSerializer, MaterialSerializer, QuestionAnswerSerializer
from .models import Category, Course, Material, Lesson, QuestionAnswer, Enrolment, LessonProgress

from rest_framework import generics, permissions
from .serializers import LessonProgressSerializer
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def category_list_create(request):
    if request.method == 'GET':
        # Allow any user to see the categories
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Require authentication
        if not request.user.is_authenticated:
            return Response({'detail': "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check admin role
        if request.user.role != 'admin':
            return Response({'detail': "Only admin can create category"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def course_list_create(request):
    if request.method == 'GET':
        category_id = request.GET.get('category')

        # If the user is authenticated and a teacher, only show their own courses
        if request.user.is_authenticated and request.user.role == 'teacher':
            courses = Course.objects.filter(instructor=request.user)
        else:
            courses = Course.objects.all()

        if category_id:
            courses = courses.filter(category_id=category_id)

        paginator = PageNumberPagination()
        paginated_courses = paginator.paginate_queryset(courses, request)
        serializer = CourseSerializer(paginated_courses, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'detail': "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.role != 'teacher':
            return Response({'detail': "Only teachers can create courses"}, status=403)
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_detail (request,pk):
    # print("Authenticated:", request.user.is_authenticated)
    # print("User:", request.user)
  try:
    course = Course.objects.get(pk =pk)
  except Course.DoesNotExist:
    return Response('Course does not exist', status=status.HTTP_404_NOT_FOUND)
#   print("Role:", request.user)
  if request.method == 'GET':
    # print("Role:", request.user.role)
    if request.user.role in ['admin', 'student'] or request.user == course.instructor:
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    return Response('Permission denied', status=status.HTTP_403_FORBIDDEN)
  elif request.method == 'PUT':
    if request.user.role != 'teacher' or request.user != course.instructor:
      return Response('Only respective teacher can update the course', status=403)
    serializer = CourseSerializer(course, data = request.data)
    if serializer.is_valid():
      serializer.save(instructor =request.user)
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    if request.user.role != 'teacher' or request.user != course.instructor:
      return Response('Only respective teacher can delete the course', status=403)
    course.delete()
    return Response("Course deleted", status=status.HTTP_204_NO_CONTENT)








@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def lesson_list_create(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not hasattr(request.user, 'role') or request.user.role != 'teacher':
            return Response({'detail': "Only teachers can create lessons."}, status=403)

        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def material_list_create(request):
    if request.method == 'GET':
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("Incoming data:", request.data)
        if not hasattr(request.user, 'role') or request.user.role != 'teacher':
            return Response({'detail': "Only teachers can create materials."}, status=403)

        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  




@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def enrolment_list_create(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        queryset = Enrolment.objects.filter(student=request.user)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        serializer = EnrolmentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['student'] = request.user.id
        serializer = EnrolmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def questionAnswer_list_create(request):
  if request.method == 'GET':
    questionAnswer = QuestionAnswer.objects.all()
    serializer = QuestionAnswerSerializer(questionAnswer, many=True)
    return Response(serializer.data)
  elif request.method =='POST':
    serializer = QuestionAnswerSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  





class MarkLessonCompletedAPIView(generics.CreateAPIView):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student = request.user
        lesson_id = request.data.get('lesson')

        if not lesson_id:
            return Response({"detail": "Lesson ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, id=lesson_id)
        progress, created = LessonProgress.objects.get_or_create(
            student=student,
            lesson=lesson,
            defaults={"is_completed": True}
        )

        if not created:
            progress.is_completed = not progress.is_completed
            progress.save()

        return Response({
            "lesson": lesson.id,
            "is_completed": progress.is_completed
        }, status=status.HTTP_200_OK)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    course_id = request.data.get('course_id')
    course = get_object_or_404(Course, id=course_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(course.price * 100),  
                'product_data': {
                    'name': course.title,
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        customer_email=request.user.email,
        success_url = settings.STRIPE_SUCCESS_URL + f'?course_id={course.id}',
        cancel_url=settings.STRIPE_CANCEL_URL,
    )

    return Response({'id': session.id})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_enrolment(request):
    course_id = request.data.get('course_id')
    if not course_id:
        return Response({"error": "course_id is required"}, status=400)

    course = get_object_or_404(Course, id=course_id)

    enrolment, created = Enrolment.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={"price": course.price}
    )
    enrolment.is_active = True
    enrolment.save()

    return Response({"success": True, "enrolment_id": enrolment.id})