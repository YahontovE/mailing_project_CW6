from django.contrib import admin

from mailing.models import Client, Mailing, MessageMailing, LogMailing


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('ferst_name','last_name','email',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time','end_time','status',)

@admin.register(MessageMailing)
class MessageMailingAdmin(admin.ModelAdmin):
    list_display = ('title','body',)


@admin.register(LogMailing)
class LogMailinggAdmin(admin.ModelAdmin):
    list_display = ('last_mailing','status_try','answer_mail_server',)
