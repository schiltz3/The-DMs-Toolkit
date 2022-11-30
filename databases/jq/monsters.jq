[.[] | 
{
  model: "toolkit.monster",
  pk: .name,
  fields: {
    Challenge_Rating: .cr,
    Size: .size,
    Type: .type,
    Alignment: .alignment,
    Armor_Class: .ac,
    Hitpoints: .hp,
    Initiative: .init,
    Creature_Tags:
      [
        if .tags == "" then empty else .tags | split(", ") | .[] end,
        if .environment == "" then empty else .environment | split(", ") | .[] end,
        if ."lair?" == "" then empty else ."lair?" end,
        if .unique == "" then empty else .unique end,
        if .legendary == "" then empty else .legendary end
      ],
      Source: .sources
  }
}]