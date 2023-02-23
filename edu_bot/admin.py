from django.contrib import admin
from .models import Student, Teacher, TestResponse, Group, TestKeys
# Register your models here.


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(TestKeys)
admin.site.register(TestResponse)
