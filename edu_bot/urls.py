from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

router = DefaultRouter()
router.register(r'students', StudentAPIView, basename='students')
router.register(r'teachers', TeacherAPIView, basename='teachers')
router.register(r'groups', GroupAPIView, basename='groups')
router.register(r'tests', TestAPIView, basename='tests')
router.register(r'testresponse', TestResponseAPIView, basename='testresponse')
urlpatterns = router.urls

# urlpatterns = [
#     path("students/", StudentAPIView.as_view(), name='students'),
#     path("tests/", TestAPIView.as_view(), name='tests'),
#     path("testresponse/", TestResponseAPIView.as_view(), name='testresponse'),
#     # path("results/", ResultsAPIView.as_view(), name='results'),
# #     path('testresponse/A/', TestResponseBAPIView.as_view(), name='testresponseb'),
# ]


