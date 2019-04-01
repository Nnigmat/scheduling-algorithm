from django.db import models
from django.core.validators import validate_email, MaxValueValidator, MinValueValidator

class Faculty(models.Model):
    '''
    ' Faculty model
    '''
    email = models.EmailField(verbose_name='E-mail', max_length=254, blank=False, unique=True, validators=[validate_email])
    name = models.CharField(verbose_name='Name', max_length=50)
    surname = models.CharField(verbose_name='Surname', max_length=50)

class Prof(Faculty):
    pass

class TA(Faculty):
    pass

class Course(models.Model):
    '''
    ' Course model
    '''
    name = models.CharField(verbose_name='Course', default='Course', max_length=50, unique=True, blank=False)
    class_num = models.IntegerField(verbose_name='Number of classes', default=100, max_length=1000, null=False, editable=True)
    year = models.IntegerField(default=1, max_length=10)
    professors = models.ManyToManyField(Prof)
    tas = models.ManyToManyField(TA)

class Auditorium(models.Model):
    '''
    ' Auditorium model
    '''
    capacity = models.IntegerField(verbose_name='Capacity', default=100, null=False, editable=True, 
        validators=[MaxValueValidator(999), MinValueValidator(100)])
    number = models.IntegerField(verbose_name='Auditorium number', max_length=1000, null=False,
        unique=True, editable=True)

class StudentGroup(models.Model):
    pass

class AdditionalProperties(models.Model):
    '''
    ' AdditionalProperties model
    '''
    pass
    
class Preferences(models.Model):
    '''
    ' Preferendes model
    '''
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE, primary_key=True)

class Schedule(models.Model):
    '''
    ' Schedule model
    '''
    res = models.CharField(max_length=2048, blank=False)













    
    # created = models.CharField(max_length=120, blank=False, null=False, editable=True)
