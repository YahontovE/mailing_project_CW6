from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}

class Blog(models.Model):
        title = models.CharField(max_length=100, verbose_name='заголовок',**NULLABLE)
        description = models.TextField(verbose_name='содержимое',**NULLABLE)
        image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
        create_date = models.DateField(auto_now_add=True, verbose_name='дата создания',**NULLABLE)
        count_views = models.IntegerField(verbose_name='количество просмотров', default=0)

        def __str__(self):
            return self.title

        class Meta:
            verbose_name = 'Блог'
            verbose_name_plural = 'Блоги'
