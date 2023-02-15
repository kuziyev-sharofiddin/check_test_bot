from django.shortcuts import render
from .serializers import *
from rest_framework.generics import ListAPIView
from .models import *
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from django.db.models import Q
# from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class StudentFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    login = filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Student
        fields = ['name','login']
    

class TeacherFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Teacher
        fields = ['first_name']

class GroupFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    teacher = filters.CharFilter(lookup_expr="id")
    
    class Meta:
        model = Group
        fields = ['name', 'teacher']
        
        

class TestFilter(filters.FilterSet):
    message = filters.CharFilter(lookup_expr="icontains")
    name = filters.CharFilter(lookup_expr='icontains')
    group = filters.CharFilter(lookup_expr="id")
    
    class Meta:
        model = Test
        fields = ['message','group','name']


class TestResponseFilter(filters.FilterSet):
    message = filters.CharFilter(lookup_expr="icontains")
    group = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = TestResponse
        fields = ['message','group']
    


# class TeacherViewSet(viewsets.ModelViewSet):

#     serializer_class = TeacherSerializer
#     queryset = Teacher.objects.all()
#     filter_backends = (DjangoFilterBackend, SearchFilter)
#     filter_fields = ("id", "name")
   
# class GroupViewSet(viewsets.ModelViewSet):
    
#     serializer_class = GroupSerializer
#     queryset = Group.objects.all()
   
class TeacherAPIView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_fields = ("id", "name")
    filterset_class = TeacherFilter
 
class StudentAPIView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_fields = ("id", "name",'login')
    filterset_class = StudentFilter
  
class GroupAPIView(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    filter_fields = ("id", "name",'teacher')
    filterset_class = GroupFilter
     
class TestAPIView(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    filter_fields = ("id", "message",'group','name')
    filterset_class = TestFilter 
    
class TestResponseAPIView(viewsets.ModelViewSet):
    serializer_class = TestResponseSerilizer
    queryset = TestResponse.objects.all()
    filter_fields = ("id", "message",'group')
    filterset_class = TestResponseFilter 
    
