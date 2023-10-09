from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    ferst_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, **NULLABLE, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта', unique=True)
    coment = models.TextField(**NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', **NULLABLE)

    def __str__(self):
        return f'{self.ferst_name} {self.email} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    PERIOD_DAILY = 'dally'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'ежедневно'),
        (PERIOD_WEEKLY, 'еженедельно'),
        (PERIOD_MONTHLY, 'ежемесечно'),
    )

    STATUS_CREATE = 'create'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUS = (
        (STATUS_CREATE, 'создана'),
        (STATUS_STARTED, 'запущена'),
        (STATUS_DONE, 'завершена'),
    )

    time = models.TimeField(verbose_name='Время рассылки',**NULLABLE)
    start_time = models.TimeField(verbose_name='Начало рассылки')
    end_time = models.TimeField(verbose_name='Конец срассылки')
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    period = models.CharField(max_length=50, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Дата рассылки')
    status = models.CharField(max_length=50, choices=STATUS, default=STATUS_CREATE, **NULLABLE,
                              verbose_name='Статус рассылки')

    #message = models.ForeignKey('MessageMailing', on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', **NULLABLE)

    def __str__(self):
        return f'{self.status} {self.client}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MessageMailing(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема Расслыки')
    body = models.TextField(verbose_name='Текста рассылки')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE, verbose_name='Рассылка')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.body}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class LogMailing(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILD = 'faild'
    STATUS_TRY = (
        (STATUS_OK, 'успешно'),
        (STATUS_FAILD, 'ошибка'),
    )
    settings = models.ForeignKey(Mailing, on_delete=models.CASCADE,**NULLABLE, verbose_name='Рассылка')


    last_mailing = models.DateTimeField(auto_now_add=True, verbose_name='Последняя рассылка')
    status_try = models.CharField(max_length=20, choices=STATUS_TRY, verbose_name='Статус попытки')
    answer_mail_server = models.BooleanField(verbose_name='Ответ сервера',**NULLABLE)

    def __str__(self):
        return f'{self.last_mailing} {self.status_try} {self.answer_mail_server}'

    class Meta:
        verbose_name = 'Логи'
        verbose_name_plural = 'Логи'


'''Клиент сервиса:
контактный email,
ФИО,
комментарий.
-Рассылка (настройки):
время рассылки;
периодичность: раз в день, раз в неделю, раз в месяц;
статус рассылки: завершена, создана, запущена.
-Сообщение для рассылки:
тема письма,
тело письма.
-Логи рассылки:
дата и время последней попытки;
статус попытки;
ответ почтового сервера, если он был.
jahontoveu@yandex.ru'''
