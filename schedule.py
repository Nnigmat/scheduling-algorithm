import random
class Course:
    def __init__(self, name, classes_num, profs, tas, year):
        self.name = name
        self.type = type
        self.classes_num = classes_num
        self.profs = profs
        self.tas = tas
        self.year = year

class Class:
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

class Faculty(User):
    def __init__(self, type, name):
        super().__init__()
        self.courses = []
        self.type = type
        self.name = name

class StudentGroup(User):
    def __init__(self, year, num):
        super().__init__()
        self.year = year
        self.num = num

class TimeSlot:
    def __init__(self, day, time_start):
        self.day = day
        self.time_start = time_start



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
profs.append(Faculty(name="Bobrov", type="TA"))
profs.append(Faculty(name="Kanatov", type="TA"))
profs.append(Faculty(name="Succi", type="TA"))
profs.append(Faculty(name="Gorodetski", type="TA"))


tas = []
tas.append(Faculty(name="TA1", type="TA"))
tas.append(Faculty(name="TA2", type="TA"))
tas.append(Faculty(name="TA3", type="TA"))

courses = []
courses.append(Course(name="SWP", classes_num=3, profs=[profs[0]], tas=[tas[0]], year=2))
courses.append(Course(name="DMD", classes_num=3, profs=[profs[1]], tas=[tas[1]], year=2))
courses.append(Course(name="Networks", classes_num=3, profs=[profs[2]], tas=[tas[0]], year=2))
courses.append(Course(name="Probstat", classes_num=3, profs=[profs[3]], tas=[tas[2]], year=2))

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
print(out)
