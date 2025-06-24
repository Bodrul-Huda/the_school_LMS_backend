
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializers
from .models import Category, Course, Material, Lesson, QuestionAnswer, Enrolment, LessonProgress



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'is_active', 'created_at', 'updated_at']



class MaterialSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Material
        fields = ['id', 'title', 'description', 'file_type', 'file', 'course', 'is_active', 'created_at', 'updated_at']



class LessonSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video', 'course', 'is_active', 'is_completed', 'created_at', 'updated_at']

    
    def get_is_completed(self, lesson):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return LessonProgress.objects.filter(student=request.user, lesson=lesson, is_completed=True).exists()


class CourseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='teacher')
    )
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        rep['instructor'] = UserSerializers(instance.instructor).data
        return rep

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be zero or more.")
        return value



class QuestionAnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()

    class Meta:
        model = QuestionAnswer
        fields = ['id', 'user', 'lesson', 'description', 'is_active', 'created_at', 'updated_at']



class EnrolmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)
    course_details = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Enrolment
        fields = [
            'id', 'student', 'course', 'is_active', 'price', 'progress', 'course_details',
            'is_complete', 'total_mark', 'is_certificate_ready', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')
        if Enrolment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Student is already enrolled in this course.")
        return data



class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['lesson']
        read_only_fields = ['completed_at']




