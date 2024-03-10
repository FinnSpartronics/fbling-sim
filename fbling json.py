from enum import Enum

# Read file
with open('show.fbling') as f:
    lines = f.readlines()

# Strips the lines
i = 0
for ln in lines:
    lines[i] = ln.replace("\n", "").strip()
    i += 1

print(lines)

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
print(f"{title} - {desc} - Version {ver} fBling")

class Segment:
    def __init__(self, time, rFunc, gFunc, bFunc, wrap):
        self.time = time
        self.r = rFunc
        self.g = gFunc
        self.b = bFunc
        self.wrap = wrap
    def dict(self):
        return {
            "function": {
                "r": self.r,
                "g": self.g,
                "b": self.b,
                "wrapping": self.wrap
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
for l in lines[verIndex+1:]:
    if (partOn == ReadPartOn.INIT or partOn == ReadPartOn.SEARCHING) and l.startswith("-"):
        if partOn == ReadPartOn.SEARCHING:
            segments.append(Segment(time=currentSeg["time"],
                                    rFunc=currentSeg["red"],
                                    gFunc=currentSeg["green"],
                                    bFunc=currentSeg["blue"],
                                    wrap="wrap" in currentSeg).dict())
        currentSeg = {"time": float(l[1:].strip())}
        partOn = ReadPartOn.RED
    elif partOn == ReadPartOn.RED:
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

print(segments)