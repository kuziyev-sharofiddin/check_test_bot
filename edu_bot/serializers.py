from rest_framework import serializers
from .models import Teacher,Group,Student,Test,TestResponse


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        
class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta: 
        model = Student
        fields = "__all__"
        


class TestSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    teacher = TeacherSerializer()
    class Meta:
        model = Test
        fields = "__all__"
        
class TestResponseSerilizer(serializers.ModelSerializer):
    student = StudentSerializer()
    test = TestSerializer()
    class Meta:
        model = TestResponse
        fields = "__all__"