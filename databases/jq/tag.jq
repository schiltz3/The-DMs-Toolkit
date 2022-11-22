[.[].fields.Creature_Tags] | flatten | unique 
| map(
    {
        "model": "toolkit.tag",
        "pk":.
        
    }
)