####Finn's Bling
#fBling
###1 - What is fBling?
fBling lets you write light shows to be replayed by an AddressableLED for FRC use.

---

###2 - How to use fBling simulator
Create a show.json file in the same directory as main.py and run main.py\
A simulator window will open and replay your light show.

####2.1 - How do I make the JSON file?
A converter will be added soon to change .fbling files to .json files for use in the simulator.\
You can also manually create your own JSON files. Here is the format for a version 1 fBling JSON:
```json
{
  "title": "",
  "description": "",
  "version": 1,
  "segments": [
    {
      "function": {
        "r": "0",
        "g": "0",
        "b": "0",
        "wrapping": true
      },
      "time": 0
    }
  ]
}
```
You may add more segments to the array.\
Include your functions in the R, G, and B strings.\
If you do not wish to include wrapping, you may omit the line from that segment.\
Times are in seconds.

####2.2 - How to turn a JSON into .fbling?
Use the converter

---

###3 - .fBling syntax and format
fBling files are the way fBling light shows are stored.
```fbling
#Name
#Description
#Version Number
-0                  // Time that segment begins
0                   // Red function
0                   // Green function
0                   // Blue Function
wrap                // Include if you want wrapping
-1
...
```
fBling is primarily based around newlines.\
The header, the first three lines, contains the name, description, and version number, respectively. They must be started out with a #.\

Custom global utility functions are coming soon

####3.1 Variables
| Variable Name | Brief Description |
| --- | --- |
| i | The pixel number|
| f | The current frame. fBling runs at 20fps |
| len | The length of the light strip. default: 50 |
| t | The current time in seconds |
| rt | The time since the current segment began |