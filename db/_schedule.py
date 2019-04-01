import random
from .models import Faculty, Course, AdditionalProperties
class _Course:
    def __init__(self, name, classes_num, profs, tas, year):
        self.name = name
        self.classes_num = classes_num
        self.profs = profs
        self.tas = tas
        self.year = year

class _Class:
    def __init__(self, course, type, group=None):
        self.course = course
        self.type = type
        self.group = group
        self.time = None

class User:
    def __init__(self):
        self.class_time = []

    def set_time(self, class_time):
        self.class_time.append(class_time)

    def isBusy(self, time):
        return time in self.class_time

class _Faculty(User):
    def __init__(self, type, name):
        super().__init__()
        self.courses = []
        self.type = type
        self.name = name

class _StudentGroup(User):
    def __init__(self, year, num):
        super().__init__()
        self.year = year
        self.num = num

class _TimeSlot:
    def __init__(self, day, time_start):
        self.day = day
        self.time_start = time_start


def generate_schedule():
    time_slots = []
    for i in range(0, 5):
        time_slots.append(TimeSlot(i, "9:00"))
        time_slots.append(TimeSlot(i, "10:35"))
        time_slots.append(TimeSlot(i, "12:10"))
        time_slots.append(TimeSlot(i, "14:10"))
        time_slots.append(TimeSlot(i, "15:45"))
        time_slots.append(TimeSlot(i, "17:20"))
        time_slots.append(TimeSlot(i, "18:55"))

    profs = []
    for prof in Faculty.objects.filter(type='Professor'):
        profs.append(_Faculty(name=prof.name, type='Professor'))

    tas = []
    for ta in Faculty.objects.filter(type'TA'):
        tas.append(_Faculty(name=ta.name, type='TA'))

    courses = []
    i = 0
    for course in Course.objects.all():
        courses.append(_Course(name=course.name,  classes_num=course.classes_num, profs=[profs[i]], tas=[tas[i]], year=course.year))
        i += 1

    groups = []
    groups.append(StudentGroup(2, 1))
    groups.append(StudentGroup(2, 2))
    groups.append(StudentGroup(2, 3))

    classes = []
    classes.append(Class(course=courses[0], type="Lecture"))
    classes.append(Class(course=courses[0], type="Lab", group=groups[0]))
    classes.append(Class(course=courses[0], type="Lab", group=groups[1]))
    classes.append(Class(course=courses[0], type="Lab", group=groups[2]))
    classes.append(Class(course=courses[0], type="Lab", group=groups[0]))
    classes.append(Class(course=courses[0], type="Lab", group=groups[1]))
    classes.append(Class(course=courses[0], type="Lab", group=groups[2]))

    classes.append(Class(course=courses[1], type="Lecture"))
    classes.append(Class(course=courses[1], type="Tutorial"))
    classes.append(Class(course=courses[1], type="Lab", group=groups[0]))
    classes.append(Class(course=courses[1], type="Lab", group=groups[1]))
    classes.append(Class(course=courses[1], type="Lab", group=groups[2]))

    classes.append(Class(course=courses[2], type="Lecture"))
    classes.append(Class(course=courses[2], type="Tutorial"))
    classes.append(Class(course=courses[2], type="Lab", group=groups[0]))
    classes.append(Class(course=courses[2], type="Lab", group=groups[1]))
    classes.append(Class(course=courses[2], type="Lab", group=groups[2]))

    classes.append(Class(course=courses[3], type="Lecture"))
    classes.append(Class(course=courses[3], type="Tutorial"))
    classes.append(Class(course=courses[3], type="Lab", group=groups[0]))
    classes.append(Class(course=courses[3], type="Lab", group=groups[1]))
    classes.append(Class(course=courses[3], type="Lab", group=groups[2]))


    for i in range(0, len(courses)):
        for j in range(0,len(profs)):
            if profs[j].name in courses[i].profs:
                profs[j].courses.append(courses[i])
    out = []
    i = 0
    while i < len(classes):
        time = int(random.uniform(0, len(time_slots)))
        classes[i].time = time_slots[time]
        clash = False
        for j in range(0, len(classes[i].course.profs)):
            if classes[i].course.profs[j].isBusy(time_slots[time]):
                clash = True
                break
        for j in range(0, len(classes[i].course.tas)):
            if classes[i].course.tas[j].isBusy(time_slots[time]):
                clash = True
                break
        if classes[i].group != None:
            if classes[i].group.isBusy(time_slots[time]):
                clash = True
        else:
            for j in range(0, len(groups)):
                if groups[j].year == classes[i].course.year:
                    if groups[j].isBusy(time_slots[time]):
                        clash = True
        if not clash:
            for j in range(0, len(classes[i].course.profs)):
                classes[i].course.profs[j].set_time(time_slots[time])
            for j in range(0, len(classes[i].course.tas)):
                classes[i].course.tas[j].set_time(time_slots[time])
            if classes[i].group != None:
                classes[i].group.set_time(time_slots[time])
            else:
                for j in range(0, len(groups)):
                    groups[j].set_time(time_slots[time])
            if classes[i].group == None:
                out.append(classes[i].course.name + " " + classes[i].type + " " + str(time_slots[time].day) +  " " + time_slots[time].time_start)
            else:
                out.append(classes[i].course.name + " " + classes[i].type + " day " + str(time_slots[time].day) +  " " + time_slots[time].time_start + " group " + str(classes[i].group.num))
            i += 1

    return out
