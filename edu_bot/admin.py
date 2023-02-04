from django.contrib import admin
from .models import Student, Teacher, Test,TestResponse, Group
# Register your models here.


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Test)
admin.site.register(TestResponse)