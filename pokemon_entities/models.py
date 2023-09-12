from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя покемона")
    picture = models.ImageField(verbose_name="Изображение покемона")
