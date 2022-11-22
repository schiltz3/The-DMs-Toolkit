def frac(f):
  if f == "1/2" then .5
  else
    if f == "1/4" then .25
    else
      if f == "1/8" then .125
      else f
      end
    end
  end;

[.[] | 
{
  model: "toolkit.Monster",
  pk: .name,
  fields: {
    Challenge_Rating: frac(.cr),
    Size: .size,
    Type: .type,
    Alignment: .alignment,
    Armor_Class: .ac,
    Hitpoints: .hp,
    Initiative: .init,
    Creature_Tags:
      [
        if .unique == "" then empty else .unique end,
        if .environment == "" then empty else .environment | split(", ") | .[] end,
        if .legendary == "" then empty else .legendary end,
        if .tags == "" then empty else .tags end,
        if ."lair?" == "" then empty else ."lair?" end
      ],
      Source: .sources
  }
}]