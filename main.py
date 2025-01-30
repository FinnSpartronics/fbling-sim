import pygame, time, json, conversions, math, colorsys, random
pygame.init()

font = pygame.font.SysFont('Comic Sans MS', 24)
fontsmall = pygame.font.SysFont('Comic Sans MS', 16)

frame = 0
on = 0
segment = None
running = True

show = conversions.convertfBlingJson('show.fbling')
pygame.display.set_caption(f"fBling Sim - {show['title']} - {show['description']} - fBling v{show['version']}")
show = show["segments"]

with open('config.json') as f:
    config = json.load(f)
debugMode = config["DEBUG"]

pixelCount = config["LENGTH"]
led_width = config["LED_WIDTH"]
height = config["LED_HEIGHT"]

screenWidth = pixelCount*led_width
if config["FRAME"]:
    screen = pygame.display.set_mode([screenWidth, height])
else:
    screen = pygame.display.set_mode([screenWidth+8, height+8], pygame.NOFRAME)

def drawPixels(func, pixels = pixelCount):
    pw = led_width
    if config["FRAME"]:
        for i in range(pixels):
            pygame.draw.rect(screen, makeColorReal(func(i)), pygame.Rect(pw*(i),0,pw,height))
    else:
        for i in range(pixels):
            pygame.draw.rect(screen, makeColorReal(func(i)), pygame.Rect(4+(pw*(i)),4,pw,height))

def clamp(a,mi,ma):
    return min(max(a,mi),ma)

def clamp255(n):
    return clamp(n,0,255)

def clamp1(n):
    return clamp(n,0,1)

def makeColorReal(c):
    if "hsv" in segment["function"]:
        if segment["function"]["hsv"]:
            if "wrapping" in segment["function"]:
                if segment["function"]["wrapping"]:
                    def wrapClampHSV(x):
                        if x == 0: return 0
                        if x < 0:
                            return (x - 0.000001) % 1
                        return (x - 0.000001) % 1
                    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(wrapClampHSV(c[0]/360), wrapClampHSV(c[1]/100), wrapClampHSV(c[2]/100)))
            return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(clamp1(c[0]/360), clamp1(c[1]/100), clamp1(c[2]/100)))
    if "wrapping" in segment["function"]:
        if segment["function"]["wrapping"]:
            def wrapClamp(x):
                if x == 0: return 0
                if x < 0:
                    return int((x - 0.1) % 255)
                return int((x - 0.1) % 255)

            return (wrapClamp(c[0]), wrapClamp(c[1]), wrapClamp(c[2]))
    return (int(clamp255(c[0])), int(clamp255(c[1])), int(clamp255(c[2])))

def color(i):
    x = (((i+frame) % 3)+1)*(255/4)
    return (x, 0, 2*x)

def tmp(i):
    return (evalF(segment["function"]["r"], i, frame, pixelCount),
     evalF(segment["function"]["g"], i, frame, pixelCount),
     evalF(segment["function"]["b"], i, frame, pixelCount))

def cfunction(i):
    if type(segment["function"]) == "str": return eval(segment["function"].replace(""))
    return (evalF(segment["function"]["r"], i, frame, pixelCount),
            evalF(segment["function"]["g"], i, frame, pixelCount),
            evalF(segment["function"]["b"], i, frame, pixelCount))

def evalF(function,i,frame,length):
    getCurrentSegment()
    random.seed((segmentIndex * 2001) + i)
    f = conversions.convertToInternalMath(function)
    f = (f.replace("i",str(i)).replace("f",str(frame)).replace("len",str(length)).replace("rt",str((frame/50)-segment["time"])).replace("t",str(frame/50)))
    f = conversions.convertBackToReal(f)
    return eval(f)

segmentIndex = 0
def getCurrentSegment():
    global on, frame, segmentIndex

    sec = frame/50
    lastSeg = None

    on = 0
    for seg in show:
        if sec < seg["time"]:
            segmentIndex = show.index(seg)
            return lastSeg
        if seg == show[-1]:
            on += 1
            if "goto" in seg:
                frame = max(math.floor(eval(str(seg["goto"])) * 50), 0)
                print(f"Gone back to frame {frame} aka {frame/50}s")
                return getCurrentSegment()
            return seg
        lastSeg = seg
        on += 1

def drawText(screen, font, text, color, outline, pos, outlineSize = 2):
    surface = font.render(text, False, color)
    outSurface = font.render(text, False, outline)
    screen.blit(outSurface, (pos[0]+outlineSize,pos[1]+outlineSize))
    screen.blit(outSurface, (pos[0]-outlineSize,pos[1]+outlineSize))
    screen.blit(outSurface, (pos[0]-outlineSize,pos[1]-outlineSize))
    screen.blit(outSurface, (pos[0]+outlineSize,pos[1]-outlineSize))
    screen.blit(surface, pos)

def export():
    global frame, segment
    lastFrame = 0

    arr1 = []
    while True:
        segment = getCurrentSegment()
        if not(lastFrame == frame): break
        currArray = []
        for i in range(pixelCount):
            for c in makeColorReal(cfunction(i)):
                currArray.append(max(min(c,255),1))
        arr1.append(currArray)
        frame += 1
        lastFrame = frame

    arr = []
    for x in arr1:
        for x1 in x:
            arr.append(x1)
        arr.append(0)

    f = open(f"export{pixelCount}.bling", "wb")
    f.write(bytes(arr))
    f.close()
    print("Exported")

#drawText(screen, font, "Exporting", (255,255,255), (50,50))
if config["EXPORT"]:
    export()
else: print("no export")

while running:
    frame += 1
    time.sleep(1/50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False

    screen.fill((0, 0, 0))

    segment = getCurrentSegment()
    drawPixels(func=cfunction)

    if debugMode:
        drawText(screen, font, f"{on-1}", (0,0,0), (255,255,255), (5,0))                                   # Segment on
        drawText(screen, fontsmall, f"{frame}", (0,0,0), (255,255,255), (5,60), outlineSize=1)             # Frame on
        drawText(screen, fontsmall, f"{frame/50}s", (0,0,0), (255,255,255), (5,80), outlineSize=1)         # Time

    pygame.display.flip()

pygame.quit()