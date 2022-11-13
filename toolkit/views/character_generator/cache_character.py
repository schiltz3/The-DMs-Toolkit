from django.contrib.auth.models import User
from toolkit.models import Character

from toolkit.views.character_generator.character_elements import (
    GenerateCharacterInputs,
    GeneratedCharacterOutputs,
)


def cache_character(
    user: User,
    input: GenerateCharacterInputs,
    output: GeneratedCharacterOutputs,
):

    character = Character(
        Owner=user,
        Name=input.character_name.value,
        Race=input.race.value,
        Class=input.clazz.value,
        Background=input.background.value,
        Alignment=input.alignment.value,
        Level=0,
        Experience=0,
        Strength=output.strength,
        Dexterity=output.dexterity,
        Constitution=output.constitution,
        Intelligence=output.intelligence,
        Wisdom=output.wisdom,
        Charisma=output.charisma,
    )
    # one to one relationships get fields passed though at runtime
    cache = user.cache.character  # type: ignore

    character.save()
    if cache is not None:
        cache.delete()
    cache = character
    user.save()


def retrieve_cached_character(self):
    pass
