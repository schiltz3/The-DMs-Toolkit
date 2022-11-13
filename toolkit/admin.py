from django.contrib import admin

# Register your models here.
from .models import (
    Armor,
    Character,
    GeneratedEncounter,
    GeneratedLoot,
    GenericItem,
    MagicItem,
    Monster,
    Tag,
    Weapon,
    Cache,
)

admin.site.register(Character)
admin.site.register(Armor)
admin.site.register(Weapon)
admin.site.register(GenericItem)
admin.site.register(MagicItem)
admin.site.register(GeneratedLoot)
admin.site.register(Tag)
admin.site.register(Monster)
admin.site.register(GeneratedEncounter)
admin.site.register(Cache)
