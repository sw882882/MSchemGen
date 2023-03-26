# MSchemGen

_An unfinished project about schematic generation outside Mindustry._

# USAGE (Parsed JSON Data)

```json
{
  "name": "MSchemGen",
  "description": "output of MSchemGen (example1.json)",
  "tags": ["[Generated Schematic]"],
  "width": 2,
  "height": 2,
  "blocks": [
    {
      "type": "micro-processor",
      "x": 0,
      "y": 0,
      "rotation": 0,
      "config": {
        "code": "op add a a 1\n",
        "links": [{ "x": 1, "y": 1, "name": "wall1" }]
      }
    },
    {
      "type": "micro-processor",
      "x": 0,
      "y": 1,
      "rotation": 0,
      "config": {
        "code": "code:example.mlog", //CONFIG IS NOT YET IMPLEMENTED DO NOT TRY TO USE
        "links": []
      }
    },
    {
      "type": "copper-wall",
      "x": 1,
      "y": 1,
      "rotation": 0,
      "config": 0
    }
  ]
}
```

# USAGE (Command Line)

- For the blueprint version:

  ```
  python blueprint/main.py <your-json-file-here>
  ```

  no debug:

  ```
  python blueprint/main.py <your-json-file-here> > /dev/null
  ```

  a file named `a.msch` will appear.
