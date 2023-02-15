from django.db import models
from django.db.models.signals import pre_delete, pre_save



class Teacher(models.Model):
    user_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return str(self.first_name)

class Group(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
 
    
class Student(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True)
    login = models.CharField(max_length=50,null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name 
    

class Test(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.CharField(max_length=500, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

  
    def __str__(self):
        return f"{str(self.teacher)} {str(self.name)}"

class TestResponse(models.Model):
    answer_message = models.CharField(max_length=200, null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    correct_response_count = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
   
    
    def __str__(self):
        return str(self.answer_message)
    
    

    
    

    
     

    