from django.db import models
from django.core.validators import validate_email, MaxValueValidator, MinValueValidator

class Faculty(models.Model):
    email = models.EmailField(verbose_name='E-mail', max_length=254, blank=False, unique=True,
        validators=[validate_email])
    name = models.CharField(verbose_name='Name', max_length=50)
    surname = models.CharField(verbose_name='Surname', max_length=50)

class Course(models.Model):
    course = models.CharField(verbose_name='Course', default='Course', max_length=50, unique=True, blank=False)
    n_lecture = models.IntegerField(verbose_name='Number of students on lectures', default=100, max_length=1000, null=False,
        editable=True)
    n_lab = models.IntegerField(verbose_name='Number of students on labs', default=100, max_length=1000, null=False,
        editable=True)
    faculties = models.ManyToManyField(Faculty)

class Auditorium(models.Model):
    capacity = models.IntegerField(verbose_name='Capacity', default=100, null=False, editable=True, 
        validators=[MaxValueValidator(999), MinValueValidator(100)])
    number = models.IntegerField(verbose_name='Auditorium number', max_length=1000, null=False,
        unique=True, editable=True)

class AdditionalProperties(models.Model):
    pass
    
class Preferences(models.Model):
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE, primary_key=True)
