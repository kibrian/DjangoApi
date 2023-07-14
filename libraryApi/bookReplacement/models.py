from django.db import models

# Create your models here.

from django.db import models

class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    title =models.CharField(max_length=250)
    # Add other fields as needed

class Student(models.Model):
    # Add fields for the student
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)

class Request(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
