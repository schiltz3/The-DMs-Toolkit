from typing import Optional

from django.contrib.auth.models import User
from toolkit.cache import get_cache

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
    """Create and cache a character from the character_generator view

    Args:
        user (User): User to cache the character on
        char_input (GenerateCharacterInputs): User inputs to save in the character
        char_output (GeneratedCharacterOutputs): Generated stats to save in the character
    """

    character = Character(
        Owner=user,
        Name=char_input.character_name.value,
        Race=char_input.race.value,
        Class=char_input.clazz.value,
        Background=char_input.background.value,
        Alignment=char_input.alignment.value,
        Level=1,
        Experience=0,
        Strength=char_output.strength,
        Dexterity=char_output.dexterity,
        Constitution=char_output.constitution,
        Intelligence=char_output.intelligence,
        Wisdom=char_output.wisdom,
        Charisma=char_output.charisma,
    )
    cache = get_cache(user)
    character_cache = cache.character
    if character_cache is not None:
        character_cache.delete()

    character.save()
    cache.character = character
    user.save()


def save_cached_character(user: User) -> Optional[Character]:
    """Save the cached character to the database

    Args:
        user (User): User who has the created character

    Returns:
        Optional[Character]: Character if one is cached, else None
    """
    ret = user.cache.character
    user.cache.character = None
    user.save()
    return ret


def delete_cached_character(user: User):
    """Delete cached character

    Args:
        user (User): User to delete the cache on
    """
    cache = user.cache.character
    if cache is not None:
        cache.delete()
    user.cache.character = None
    user.save()
