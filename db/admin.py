from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Faculty, Auditorium, AdditionalProperties, Course, Preferences, Schedule, TimeSlot, StudentGroup, Class
from django.urls import path
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage, send_mail
from django_version import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from string import Template
from ._schedule import generate_schedule

class MailAdmin(admin.ModelAdmin):
    change_list_template = 'admin/db/db_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_mails/', self.send_mails)
        ]
        return custom_urls + urls

    def send_mails(self, request):
        t = Template('https://docs.google.com/forms/d/e/1FAIpQLScm7Akef32OptYwfi-D-Bg06TvYBxZgM-W-pArwwFR4JLZdYw/viewform?entry.592583197=$name&entry.966480905=$surname')

        faculty = Faculty.objects.all()

        for f in faculty:
            send_mail('Schedule creation', 'Hello!\nPlease fill the form for creating good schedule for you\n' 
                + t.substitute(name=f.name, surname=f.surname), settings.EMAIL_HOST_USER,
                 [f.email], fail_silently=False)
        self.message_user(request, 'Emails was sent successfully!')
        return HttpResponseRedirect('../')

class PreferencesAdmin(admin.ModelAdmin):
    change_list_template = 'admin/db/db_preferences.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('refresh/', self.refresh)
        ]
        return custom_urls + urls

    def refresh(self, request):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('./Trygoogle-50a92384d71a.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Answers').sheet1

        Preferences.objects.all().delete()
        fields = {
                'time':'Отметка времени',
                'email':'Адрес электронной почты',
                'name':'Name',
                'surname':'Surname',
                'class time':'Preferred class time (format HH:MM)',
                'day':'Preferred day',
                'class per day':'Number of classes per day',
                'class in row':'Number of classes in a row',
        }
        records = wks.get_all_records()
        for r in records:
            if r[fields['time']] == '':
                continue

            pref = Preferences()

            fac = Faculty.objects.filter(name=r[fields['name']].strip(), surname=r[fields['surname']].strip())
            if len(fac) == 0:
                fac = Faculty.objects.filter(email=r[fields['email']].strip())

            if len(fac) == 0:
                continue

            pref.faculty = fac[0]
            pref.preferred_class_time = r[fields['class time']]
            pref.preferred_days = r[fields['day']]
            pref.classes_per_day = r[fields['class per day']] 
            pref.classes_in_row = r[fields['class in row']] 

            pref.save()

        return HttpResponseRedirect('../')

class ScheduleAdmin(admin.ModelAdmin):
    change_list_template = 'admin/db/db_schedule.html'
 
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate_schedule/', self.make_schedule)
        ]
        return custom_urls + urls

    def make_schedule(self, request):
        out = generate_schedule()

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('./Trygoogle-50a92384d71a.json', scope)
        gc = gspread.authorize(credentials)
        wsc, grps = self.draw_main(gc.open('Schedule'))

        slots = list(TimeSlot.objects.order_by('begin_time'))
        for cls, timeslot in out.items():
            if cls.type == 'Lec':
                pass
            else:
                wsc.update_cell((timeslot[0]-1)*(TimeSlot.objects.count()+1)+3+slots.index(timeslot[1]), grps.index(cls.group.__str__())+2, f'{cls.teacher}\n{cls.course.name}')

        #schedule = Schedule.objects.create(res=out)
        return HttpResponseRedirect('../')

    def draw_main(self, sh):
        for sheet in sh.worksheets():
            pass

        sheet = int(sheet.title.split('Schedule')[1])
        title = f'Schedule{sheet+1}'
        sh.add_worksheet(title=title, rows='100', cols=str(StudentGroup.objects.count()+1))
        wsc = sh.worksheet(title)
        groups = dict()
        years = []
        for year in StudentGroup.objects.order_by('year').values('year').distinct():
            groups[year['year']] = StudentGroup.objects.filter(year=year['year'])
            years.append(year['year'])

        i, year = 1, 0
        grp = []
        while i <= StudentGroup.objects.count() and year < len(years):
            
            for gr in groups[years[year]]:
                if gr.num != 0:
                    wsc.update_cell(1, i+1, f'{gr.year}-{gr.num}')
                    grp.append(gr.__str__())
                    i += 1
            year += 1
        
        cell_list = wsc.range(f'A2:A{5*(TimeSlot.objects.count()+1)+1}')
        day, counter = 0, 0
        day_changed = True
        for cell in cell_list:
            if counter % TimeSlot.objects.count() == 0 and day_changed:
                cell.value = TimeSlot.DAY_CHOICES[day][1]
                day += 1
                day_changed = False
                continue
            else:
                cell.value = TimeSlot.objects.order_by('begin_time')[counter % TimeSlot.objects.count()].begin_time
                day_changed = True

            counter += 1
        wsc.update_cells(cell_list)
        return wsc, grp


      

admin.site.site_header = 'Automatically generated scheduling algorithm'
admin.site.register(Faculty, MailAdmin)
admin.site.register(Preferences, PreferencesAdmin)
admin.site.register(Course)
admin.site.register(Auditorium)
admin.site.register(AdditionalProperties)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(TimeSlot)
admin.site.register(StudentGroup)
admin.site.register(Class)
