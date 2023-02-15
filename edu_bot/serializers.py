from rest_framework import serializers
from .models import Teacher,Group,Student,Test,TestResponse


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        
class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    class Meta:
        model = Group
        fields = "__all__"
        
class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta: 
        model = Student
        fields = "__all__"
        


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
        
class TestResponseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TestResponse
        fields = "__all__"
        
# class ResultsSerilizer(serializers.ModelSerializer):
#     group = GroupSerializer()
#     testresponse = TestResponseSerilizer()
    
#     class Meta:
#         model = Results
#         fields = "__all__"
