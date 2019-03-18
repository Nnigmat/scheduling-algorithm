from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Faculty, Auditorium, AdditionalProperties, Course, Preferences
from django.urls import path
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage, send_mail
from django_version import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from string import Template

class MailAdmin(admin.ModelAdmin):
    change_list_template = 'admin/db/db_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_mails/', self.send_mails)
        ]
        return custom_urls + urls

    def send_mails(self, request):
        t = Template('https://docs.google.com/forms/d/e/1FAIpQLScm7Akef32OptYwfi-D-Bg06TvYBxZgM-W-pArwwFR4JLZdYw/viewform?entry.592583197=$name&entry.966480905=a$surname&entry.2133507524=$email')

        for faculty in Faculty.objects.all():
            send_mail('Schedule creation', 'Hello!\nPlease fill the form for creating good schedule for you\n' + t.substitute(name=faculty.name, surname=faculty.surname, email=faculty.surname), settings.EMAIL_HOST_USER, [faculty.email], fail_silently=False)
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

        records = wks.get_all_records()
        records.pop(0)
        print(records)
        for r in records:
            for key, value in r.items():
                print(key, value)
            
        

        return HttpResponseRedirect('../')
       

admin.site.site_header = 'Automatically generated scheduling algorithm'
admin.site.register(Faculty, MailAdmin)
admin.site.register(Preferences, PreferencesAdmin)
admin.site.register(Course)
admin.site.register(Auditorium)
admin.site.register(AdditionalProperties)
