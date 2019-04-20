from .models import AdditionalProperties, Auditorium, Class, Course, Faculty, Preferences, TimeSlot, StudentGroup
from random import randint

def fitness():
    pass

def generate_schedule():
    faculty = dict()
    audi = dict()
    groups = dict()
    classes = dict()

    slots = TimeSlot.objects.count()
    for cls in Class.objects.all():
        attempt = 0
        while attempt <= 10:
            counter += 1

            # Get day and time slot
            day = randint(1, 5)
            time = TimeSlot.objects.get(pk=randint(0, slots-1))

            # Check faculty and group are not busy
            if cls.teacher in faculty and (day, time) in faculty[cls.teacher]:
                continue
            if cls.group in groups and (day, time) in groups[cls.group]:
                continue

            # Get free auditorium
            audi_attempt = 0
            auditorium = Auditorium.objects.get(pk=randint(0, Auditorium.objects.count()))
            while auditorium in audi and (day, time) in audi[auditorium] and audi_attempt <= Auditorium.objects.count():
                auditorium = Auditorium.objects.get(pk=randint(0, Auditorium.objects.count()))
                audi_attempt += 1

            # All auditoriums are busy
            if audi_attempt > Auditorium.objects.count():
                continue

            # Reserve the faculty and group day and time slot
            if cls.teacher in faculty:
                faculty[cls.teacher].append((day, time))
            else:
                faculty[cls.teacher] = [(day,time)]

            if cls.group in groups:
                groups[cls.group].append((day, time))
            else:
                groups[cls.group] = [(day,time)]

            # Store class and its time
            classes[cls] = (day, time)
            break

    return classes




            





