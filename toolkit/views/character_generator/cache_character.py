from typing import Optional

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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
    cache = user.cache.character
    if cache is not None:
        cache.delete()

    character.save()
    user.cache.character = character
    user.save()


def save_cached_character(user: User) -> Optional[Character]:
    ret = user.cache.character
    user.cache.character = None
    user.save()
    return ret


def delete_cached_character(user: User):
    cache = user.cache.character
    if cache is not None:
        cache.delete()
    user.cache.character = None
    user.save()
