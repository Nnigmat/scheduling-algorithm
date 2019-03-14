from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Faculty, Auditorium, AdditionalProperties, Course
from django.urls import path
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage, send_mass_mail

class MailAdmin(admin.ModelAdmin):
    change_list_template = 'admin/db/db_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_mails/', self.send_mails)
        ]
        return custom_urls + urls

    def send_mails(self, request):
        mails = ()
        for obj in self.model.objects.all():
            mails += EmailMessage(
                'Schedule Generation',
                'Please fill the form',
                'sche'
            )

        self.message_user(request, 'Emails was sent successfully!')
        return HttpResponseRedirect('../')

admin.site.site_header = 'Automatically generated scheduling algorithm'
admin.site.register(Faculty, MailAdmin)
admin.site.register(Course)
admin.site.register(Auditorium)
admin.site.register(AdditionalProperties)
