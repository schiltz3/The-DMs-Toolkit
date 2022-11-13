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
    char_input: GenerateCharacterInputs,
    char_output: GeneratedCharacterOutputs,
):

    character = Character(
        Owner=user,
        Name=char_input.character_name.value,
        Race=char_input.race.value,
        Class=char_input.clazz.value,
        Background=char_input.background.value,
        Alignment=char_input.alignment.value,
        Level=0,
        Experience=0,
        Strength=char_output.strength,
        Dexterity=char_output.dexterity,
        Constitution=char_output.constitution,
        Intelligence=char_output.intelligence,
        Wisdom=char_output.wisdom,
        Charisma=char_output.charisma,
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
