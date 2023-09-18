import folium
from django.utils.timezone import localtime

from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        disappeared_at__gt=current_time,
        appeared_at__lt=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.picture.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.picture.url),
            'title_ru': pokemon.name
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    current_time = localtime()
    pokemon_entities = pokemon.entities.filter(
        disappeared_at__gt=current_time,
        appeared_at__lt=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.picture.url)
        )

    pokemon_params = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.name,
        "title_en": pokemon.name_en,
        "title_jp": pokemon.name_jp,
        "description": pokemon.description,
        "img_url": request.build_absolute_uri(pokemon.picture.url)
    }

    if pokemon.previous_evolution:
        pokemon_params["previous_evolution"] = {
            "title_ru": pokemon.previous_evolution.name,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(
                pokemon.previous_evolution.picture.url)
        }

    if pokemon.next_evolutions.all().first():
        pokemon_params["next_evolution"] = {
            "title_ru": pokemon.next_evolutions.all().first().name,
            "pokemon_id": pokemon.next_evolutions.all().first().id,
            "img_url": request.build_absolute_uri(
                pokemon.next_evolutions.all().first().picture.url)
            }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_params
    })
