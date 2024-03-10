from enum import Enum

def convertfBlingJson():
    # Read file
    with open('show.fbling') as f:
        lines = f.readlines()

    # Strips the lines
    i = 0
    for ln in lines:
        lines[i] = ln.replace("\n", "").strip()
        if "//" in lines[i]:
            lines[i] = lines[i][0:lines[i].index("//")].strip()
        i += 1

    # Finds header info (Title, Description, Version)
    titleIndex = 0
    while lines[titleIndex] == "": titleIndex += 1

    descIndex = titleIndex+1
    while lines[descIndex] == "": descIndex += 1

    verIndex = descIndex+1
    while lines[verIndex] == "": verIndex += 1

    if lines[titleIndex].startswith("$") and lines[descIndex].startswith("$") and lines[verIndex].startswith("$"):
        print("Improper fBling file - Missing header.")

    title = lines[titleIndex][1:].strip()
    desc = lines[descIndex][1:].strip()
    ver = int(lines[verIndex][1:].strip())

    # Segments

    class Segment:
        def __init__(self, time, rFunc, gFunc, bFunc, wrap, useHSV):
            self.time = time
            self.r = rFunc
            self.g = gFunc
            self.b = bFunc
            self.wrap = wrap
            self.hsv = useHSV
        def dict(self):
            return {
                "function": {
                    "r": self.r,
                    "g": self.g,
                    "b": self.b,
                    "wrapping": self.wrap,
                    "hsv": self.hsv,
                },
                "time": self.time
            }
        def __str__(self):
            return self.dict()

    class ReadPartOn(Enum):
        INIT = -99,
        SEARCHING = -1,
        RED = 0,
        GREEN = 1,
        BLUE = 2,

    segments = []
    partOn = ReadPartOn.INIT
    currentSeg = {}
    goto = False
    for l in lines[verIndex+1:]:
        goto = False
        if (partOn == ReadPartOn.INIT or partOn == ReadPartOn.SEARCHING) and l.startswith("-"):
            if partOn == ReadPartOn.SEARCHING:
                segments.append(Segment(time=currentSeg["time"],
                                        rFunc=currentSeg["red"],
                                        gFunc=currentSeg["green"],
                                        bFunc=currentSeg["blue"],
                                        wrap="wrap" in currentSeg,
                                        useHSV="hsv" in currentSeg).dict())
            currentSeg = {"time": float(l[1:].strip())}
            partOn = ReadPartOn.RED
        elif partOn == ReadPartOn.RED:
            if "goto" in l:
                currentSeg["goto"] = float(l[4:].strip())
                segments.append(currentSeg)
                goto = True
                partOn = ReadPartOn.INIT
            elif "gofo" in l:
                currentSeg["goto"] = float(l[4:].strip())/20
                segments.append(currentSeg)
                goto = True
                partOn = ReadPartOn.INIT
            else:
                currentSeg["red"] = l
                partOn = ReadPartOn.GREEN
        elif partOn == ReadPartOn.GREEN:
            currentSeg["green"] = l
            partOn = ReadPartOn.BLUE
        elif partOn == ReadPartOn.BLUE:
            currentSeg["blue"] = l
            partOn = ReadPartOn.SEARCHING
        elif partOn == ReadPartOn.SEARCHING:
            if "wrap" in l: currentSeg["wrap"] = True
            if "usehsv" in l: currentSeg["hsv"] = True
    if not(goto):
        segments.append(Segment(time=currentSeg["time"],
                                rFunc=currentSeg["red"],
                                gFunc=currentSeg["green"],
                                bFunc=currentSeg["blue"],
                                wrap="wrap" in currentSeg,
                                useHSV="hsv" in currentSeg).dict())

    # Final Composition
    json = {
        "title": title,
        "description": desc,
        "version": ver,
        "segments": segments,
    }
    return json

# Variable Characters:
# i f t e
# Other variables should be fine because they are multiple characters

# jsm = Javascript required Math.
# math. = Is a math function
conversionTable = {
    "abs": "jsmabs",
    "acos": "math.acos",
    "acosh": "math.acosh",
    "asin": "math.asin",
    "asinh": "math.asinh",
    "atan": "math.atan",
    "atan2": "math.atan2",
    "atanh": "math.atanh",
    "ceil": "math.ceil",
    "cos": "math.cos",
    "cosh": "math.cosh",
    "exp": "math.exp",
    "expm1": "math.xpm1",
    "floor": "math.floor",
    "hypot": "math.hypot",
    "log": "math.log",
    "log1p": "math.log1p",
    "log2": "math.log2",
    "log10": "math.log10",
    "max": "jsmmax",
    "min": "jsmmin",
    "pow": "jsmpow",
    "round": "jsmround",
    "sin": "math.sin",
    "sinh": "math.sinh",
    "sqrt": "math.sqrt",
    "tan": "math.tan",
    "tanh": "math.tanh",
    "trunc": "math.trunc"
}
conversionTableInt = {
    "abs": "m001",
    "acos": "m002",
    "acosh": "m003",
    "asin": "m004",
    "asinh": "m005",
    "atan": "m006",
    "atan2": "m007",
    "atanh": "m008",
    "ceil": "m009",
    "cos": "m010",
    "cosh": "m011",
    "exp": "m012",
    "expm1": "m013",
    "floor": "m014",
    "hypot": "m015",
    "log": "m016",
    "log1p": "m017",
    "log2": "m018",
    "log10": "m019",
    "max": "m020",
    "min": "m021",
    "pow": "m022",
    "round": "m023",
    "sin": "m024",
    "sinh": "m025",
    "sqrt": "m026",
    "tan": "m027",
    "tanh": "m028",
    "trunc": "m029",
}

def convertToInternalMath(string):
    string = str(string.lower()).replace("pi", "3.14159")
    for key in conversionTableInt.keys():
        string = string.replace(key, conversionTableInt[key])
    return string

def convertBackToReal(string, lang="python"):
    string = str(string.lower())
    for val in conversionTableInt.values():
        string = string.replace(val, list(conversionTableInt.keys())[list(conversionTableInt.values()).index(val)])
    for key in conversionTable.keys():
        string = string.replace(key, conversionTable[key])
    if (lang == "python"):
        string = string.replace("jsm","")
    elif (lang == "javascript"):
        string = string.replace("jsm","Math.").replace("math.", "Math.")
    return string
