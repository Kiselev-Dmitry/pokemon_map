from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя покемона", null=True)
    picture = models.ImageField(verbose_name="Изображение покемона", null=True)
    description = models.TextField(blank=True)
    name_en = models.CharField(max_length=20, blank=True)
    name_jp = models.CharField(max_length=20, blank=True)

    prev_evolution = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="next_evolutions",
    )

    def __str__(self):
        return f'{self.name}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name = "entities")
    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)

    level = models.IntegerField(
        null=True,
        blank=True,
    )
    health = models.IntegerField(
        null=True,
        blank=True,
    )
    attack = models.IntegerField(
        null=True,
        blank=True,
    )
    defense = models.IntegerField(
        null=True,
        blank=True,
    )
    endurance = models.IntegerField(
        null=True,
        blank=True,
    )
