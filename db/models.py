from django.db import models
from django.core.validators import validate_email, MaxValueValidator, MinValueValidator


class Faculty(models.Model):
    FACULTY_TYPE_CHOICES = (
        ('Prof', 'Professor'),
        ('TA', 'Teacher Assistant')
    )
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(verbose_name='E-mail', max_length=254, blank=False, unique=True, validators=[validate_email])
    type = models.CharField(max_length=4, choices=FACULTY_TYPE_CHOICES)

    def __str__(self):
        return f'Faculty: {self.name} {self.surname}'


class Course(models.Model):
    name =  models.CharField(max_length=30)
    classes = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    year = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    faculty = models.ManyToManyField(Faculty)

    def __str__(self):
        return f'Course: {self.name}'


class AdditionalProperties(models.Model):
    max_class_in_row = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    

class StudentGroup(models.Model):
    year = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    num = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])

    def __str__(self):
        return f'Student group: {self.year}-{self.num}'


class TimeSlot(models.Model):
    DAY_CHOICES = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )
    begin_time = models.CharField(max_length=5)

    def __str__(self):
        return f'TimeSlot: {self.begin_time}'


class Auditorium(models.Model):
    '''
    ' Auditorium model
    '''
    capacity = models.IntegerField(verbose_name='Capacity', default=100, null=False, editable=True, validators=[MaxValueValidator(999), MinValueValidator(100)])
    number = models.IntegerField(verbose_name='Auditorium number', null=False, unique=True, editable=True, validators=[MaxValueValidator(999), MinValueValidator(100)])

    def __str__(self):
        return f'Auditorium: {self.number}'

class Preferences(models.Model):
    '''
    ' Preferendes model
    '''
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE, primary_key=True)
    preferred_class_time = models.CharField(max_length=8)
    preferred_days = models.CharField(max_length=250)
    classes_per_day = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0) ])
    classes_in_row = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0) ])


class Schedule(models.Model):
    '''
    ' Schedule model
    '''
    res = models.CharField(max_length=2048, blank=False)


class Class(models.Model):
    CLASS_CHOICES = (
        ('Lab', 'Lab'),
        ('Lec', 'Lecture'),
    )
    type = models.CharField(max_length=3, choices=CLASS_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Class: {self.type} {self.teacher} {self.group}'
