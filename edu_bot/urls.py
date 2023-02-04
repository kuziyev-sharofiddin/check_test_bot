from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

# router = DefaultRouter()
# router.register(r'teacher', TeacherViewSet, basename='teacher')
# router.register(r'group', GroupViewSet, basename='group')
# router.register(r'students', StudentViewSet, basename='students')
# router.register(r'student_id', StudentIDViewSet, basename='student_id')
# router.register(r'tests', TestViewSet, basename='tests')
# router.register(r'testresponse', TestResponseViewSet, basename='testresponse')
# urlpatterns = router.urls

urlpatterns = [
    path("students/", StudentAPIView.as_view(), name='students'),
    path("tests/", TestAPIView.as_view(), name='tests'),
    path("testresponse/", TestResponseAPIView.as_view(), name='testresponse'),
]


