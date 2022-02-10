# MSchemGen
_An unfinished project about schematic generation outside Mindustry._

# USAGE (Parsed JSON Data)
```json
{
    "name" : "hello-world", // name of schematic
    "description" : "hi-description", // desc. of schematic
    "tags" : ["tag1","tag2","useless"] // tags
    "width" : 2, // width
    "height" : 2, // height
    "blocks" : [
        {
            "type" : "router", // Type
            "x" : 0, // X
            "y" : 0, // Y
            "rotation" : 0, // Rotation
            "config" : 0 // Config (NOT SUPPORTED YET)
        },{
            "type" : "micro-processor",
            "x" : 1,
            "y" : 1,
            "rotation" : 0,
            "code" : "op add a a 1" // code of processor
            // or you can do "code:your-file"
            // processor links
            "links" : [{"x":0,"y":0,"name":"router1"},
                       {"x":0,"y":0,"name":"router2"}
                       // ...
                       ]
        }
    ]
}
```

# USAGE (Command Line)

* For the blueprint version:
    ```
    python blueprint/main.py <your-json-file-here>
    ```

    no debug:
    ```
    python blueprint/main.py <your-json-file-here> > /dev/null
    ```

    a file named `a.msch` will appear.
