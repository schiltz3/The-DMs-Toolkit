use command

monsters.jq
`jq -f ./databases/jq/monsters.jq ./databases/sources/monsters-1668973282154.json > ./databases/monsters.json`



To run the monster database through the `monsters.jq` transformation and output it to `monsters.json`

```json
{
    "Name":str,
    "Challenge_Rating":float,
    "Size":str,
    "Type":str,
    "Alignment":str,
    "Armor_Class":int,
    "Hitpoints":int,
    "Initiative":int,
    "Gold_Modifier":str,
    "Creature_Tags":str,
    "Source":str}
```
Creature_Tags is the aggregation of `unique, legendary, environment, tags and lair`

## Note:
File must use `LF` end of line sequence