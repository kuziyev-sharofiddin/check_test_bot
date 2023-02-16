from rest_framework import serializers
from .models import Teacher,Group,Student,Test,TestResponse,TestKeys


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        
class GroupDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    class Meta:
        model = Group
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        
class StudentDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    group = GroupSerializer()
    class Meta: 
        model = Student
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Student
        fields = "__all__"      


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"

class TestKeysDetailSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    test = TestSerializer()
    class Meta:
        model = TestKeys
        fields = "__all__"
        
class TestKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestKeys    
        fields = "__all__"
        

class TestResponseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TestResponse
        fields = "__all__"

class TestResponseDetailSerilizer(serializers.ModelSerializer):
    test = TestSerializer()
    student = StudentSerializer()
    class Meta:
        model = TestResponse
        fields = "__all__"
        

