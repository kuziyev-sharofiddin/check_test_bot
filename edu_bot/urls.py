from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

router = DefaultRouter()
router.register(r'teachers', TeacherAPIView, basename='teachers')
urlpatterns = router.urls

urlpatterns = [
    path("students/", StudentListAPIView.as_view(), name='students'),
    path("student_create/", StudentCreateAPIView.as_view(), name='student_create'),
    path("student/<int:pk>/", StudentRetrieveUpdateDestroyAPIView.as_view(), name='student_id'),
    
    path("groups/", GroupListAPIView.as_view(), name='groups'),
    path("group_create/", GroupCreateAPIView.as_view(), name='group_create'),
    path("group/<int:pk>/", GroupRetrieveUpdateDestroyAPIView.as_view(), name='group_id'),

    path("test_keys/", TestKeysListAPIView.as_view(), name='test_keys'),
    path("test_key_create/", TestKeysCreateAPIView.as_view(), name='test_key_create'),
    path("test_key/<int:pk>/", TestKeysRetrieveUpdateDestroyAPIView.as_view(), name='test_key_id'),

    path("test_responses/", TestResponseListAPIView.as_view(), name='test_responses'),
    path("test_response_create/", TestResponseCreateAPIView.as_view(), name='test_response_create'),
    path("test_response/<int:pk>/", TestResponseRetrieveUpdateDestroyAPIView.as_view(), name='test_response_id'),
]

urlpatterns += router.urls

