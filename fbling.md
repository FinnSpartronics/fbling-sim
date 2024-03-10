#fBling
###1 - What is fBling?
fBling (Finn's Bling) lets you write light shows to be replayed by an AddressableLED to add some Bling to your FRC robots.

---

###2 - How to use fBling simulator
Create a `show.fbling` file in the same directory as `main.py` and run `main.py`
A simulator window will open and replay your light show.

---

###3 - .fBling syntax and format
fBling files are the way fBling light shows are stored.
```fbling
#Name
#Description
#Version Number
-0                  // Time that segment begins
    0               // Red function
    0               // Green function
    0               // Blue Function
    wrap            // Include if you want wrapping
-1
...
```
fBling is primarily based around newlines.\
The header, the first three lines, contains the name, description, and version number, respectively. They must start with a #.
Indentation is not required but suggested to help improve readability.
####3.1 Variables
| Variable Name | Brief Description |
| --- | --- |
| i | The pixel number|
| f | The current frame. fBling runs at 20fps |
| len | The length of the light strip. default: 50 |
| t | The current time in seconds |
| rt | The time since the current segment began |