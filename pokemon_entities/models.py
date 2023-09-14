from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя покемона", null=True)
    picture = models.ImageField(verbose_name="Изображение покемона", null=True)

    def __str__(self):
        return f'{self.name}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()

