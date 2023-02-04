from django.shortcuts import render
from .serializers import *
from rest_framework.generics import ListAPIView
from .models import *
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
# from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class StudentFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    login = filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Student
        fields = ['name','login']
    

class TestFilter(filters.FilterSet):
    message = filters.CharFilter(lookup_expr="icontains")
    name = filters.CharFilter(lookup_expr='icontains')
    group = filters.CharFilter(lookup_expr="id")
    
    class Meta:
        model = Test
        fields = ['message','group','name']


class TestResponseFilter(filters.FilterSet):
    message = filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = TestResponse
        fields = ['message']
    


# class TeacherViewSet(viewsets.ModelViewSet):

#     serializer_class = TeacherSerializer
#     queryset = Teacher.objects.all()
#     filter_backends = (DjangoFilterBackend, SearchFilter)
#     filter_fields = ("id", "name")
   
# class GroupViewSet(viewsets.ModelViewSet):
    
#     serializer_class = GroupSerializer
#     queryset = Group.objects.all()
    
class StudentAPIView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_fields = ("id", "name",'login')
    filterset_class = StudentFilter
   
class TestAPIView(ListAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    filter_fields = ("id", "message",'group','name')
    filterset_class = TestFilter 
    
class TestResponseAPIView(ListAPIView):
    serializer_class = TestResponseSerilizer
    queryset = TestResponse.objects.all()
    filter_fields = ("id", "message")
    filterset_class = TestResponseFilter 
# class StudentIDViewSet(viewsets.ModelViewSet):

#     serializer_class = StudentIDSerializer
#     queryset = StudentID.objects.all()
    


# class TestViewSet(viewsets.ModelViewSet):

#     serializer_class = TestSerializer
#     queryset = Test.objects.all()
    
# class TestResponseViewSet(viewsets.ModelViewSet):
 
#     serializer_class = TestResponseSerilizer
#     queryset = TestResponse.objects.all()