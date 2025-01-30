#fBling v1
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
    0               // Red function (or hue)
    0               // Green function (or saturation)
    0               // Blue Function (or value)
    wrap            // Include if you want wrapping
    usehsv          // Include if you want these functions to use hsv
-1
...
```
fBling's syntax is primarily based around lines.\
The header, the first three lines, contains the name, description, and version number, respectively. They must start with a #.
Indentation is not required but suggested to help improve readability.

Most Javascript Math functions are included for use in fBling, but only if a python equivalent is also there.\
[Example] To use acos, just type:
`acos(0)` where 0 can be whatever number you want.\
Missing functions are:
- cbrt
- clz32
- fround
- imul
- sign

A random function is an intended feature in the future.

Uppercase and lowercase does not matter in fBling functions, but are taken into account for Names and Descriptions.

To add a comment to your fBling, use the `//` like in Java, Javascript, C, and other languages. Multi-line comments, `/* */` are not yet supported.

pi and e are evaluated to the 5th decimal place.

By default, fBling uses RGB255 values, but by adding `usehsv` at the end, you can use HSV values instead.


| HSV | Expected Values |
| --- |-----------------|
| Hue | 0-360           |
| Saturation | 0-100           |
| Value | 0-100           |

`wrap` and `usehsv` do not need to be on separate lines.

At the end, your final segment can be simply: `goto x` where x is a time period to loop back to.\
For example, to restart after a 10 second show:
```fBling
-10
    goto 0
```
You may also use `gofo x` to go to a specific frame.\
`goto` and `gofo` both allow calculations such as 10/2, but not variables. \
Rounding is automatically applied, as you cannot be in a partial frame, as FRC robots update 20 times a second. \
Do not attempt to go beyond the end, as that will cause issues! \
As of now, you can only put `goto` and `gofo` as the final segment, but it is in the plans to be able to put these anywhere.

#### 3.1 Variables

| Variable Name | Brief Description                          |
| --- |--------------------------------------------|
| i | The pixel number                           |
| f | The current frame. fBling runs at 50fps    |
| len | The length of the light strip. default: 50 |
| t | The current time in seconds                |
| rt | The time since the current segment began   |
| pi | 3.14159                                    |
| e | 2.71828                                    |