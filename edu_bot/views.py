from django.shortcuts import render
from .serializers import *
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import *
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from django.db.models import Q
# from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class StudentFilter(filters.FilterSet):
    name = filters.CharFilter()
    user_id = filters.CharFilter()
    group = filters.ModelChoiceFilter(field_name="group__name", queryset=Group.objects.all())
    teacher = filters.ModelChoiceFilter(field_name="teacher__first_name", queryset=Teacher.objects.all())

    
    class Meta:
        model = Student
        fields = ['name', 'user_id', 'group__name', 'teacher__first_name']
    

class TeacherFilter(filters.FilterSet):
    first_name = filters.CharFilter()
    user_id = filters.CharFilter()
    
    class Meta:
        model = Teacher
        fields = ['first_name', "user_id"]

class GroupFilter(filters.FilterSet):
    name = filters.CharFilter()
    teacher = filters.CharFilter(lookup_expr="id")

    
    class Meta:
        model = Group
        fields = ['name', 'teacher', 'id']
        
        

class TestKeysFilter(filters.FilterSet):
    name = filters.CharFilter()
    group = filters.ModelChoiceFilter(field_name="group__name", queryset=Group.objects.all())
    
    class Meta:
        model = TestKeys
        fields = ['name', 'group__name', 'teacher']



class TestResponseFilter(filters.FilterSet):
    test = filters.ModelChoiceFilter(field_name="test__name", queryset=TestKeys.objects.all())
    answer_message = filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = TestResponse
        fields = ['test__name', 'answer_message']
    

class StudentListAPIView(ListAPIView):
    serializer_class = StudentDetailSerializer
    queryset = Student.objects.all()
    filter_fields = ("id", "name", 'user_id', 'group', 'teacher')
    filterset_class = StudentFilter

class StudentCreateAPIView(CreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class StudentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherAPIView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_fields = ("id", "name")
    filterset_class = TeacherFilter

  

class GroupListAPIView(ListAPIView):
    serializer_class = GroupDetailSerializer
    queryset = Group.objects.all()
    filter_fields = ("group",'teacher','id')
    filterset_class = GroupFilter
    

class GroupCreateAPIView(CreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class GroupRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()



class TestKeysListAPIView(ListAPIView):
    serializer_class = TestKeysDetailSerializer
    queryset = TestKeys.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TestKeysFilter

class TestKeysCreateAPIView(CreateAPIView):
    serializer_class = TestKeysSerializer
    queryset = TestKeys.objects.all()

class TestKeysRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TestKeysSerializer
    queryset = TestKeys.objects.all()



class TestResponseListAPIView(ListAPIView):
    serializer_class = TestResponseDetailSerilizer
    queryset = TestResponse.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TestResponseFilter 
    

class TestResponseCreateAPIView(CreateAPIView):
    serializer_class = TestResponseSerilizer
    queryset = TestResponse.objects.all()


class TestResponseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TestResponseSerilizer
    queryset = TestResponse.objects.all()

