import pygame, time, json, conversions
pygame.init()

screen = pygame.display.set_mode([900, 100])
font = pygame.font.SysFont('Comic Sans MS', 24)
fontsmall = pygame.font.SysFont('Comic Sans MS', 16)

pixelCount = 50
frame = 0
on = 0
segment = None
running = True

show = conversions.convertfBlingJson()
pygame.display.set_caption(f"fBling Sim - {show['title']} - {show['description']} - fBling v{show['version']}")
show = show["segments"]

def drawPixels(func, pixels = pixelCount):
    pw = screen.get_width()/pixels
    for i in range(pixels):
        pygame.draw.rect(screen, makeColorReal(func(i)), pygame.Rect(pw*(i),0,pw,100))

def clamp(a,mi,ma):
    return min(max(a,mi),ma)

def clamp255(n):
    return clamp(n,0,255)

def makeColorReal(c):
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
    return eval(function.replace("i",str(i)).replace("f",str(frame)).replace("len",str(length)).replace("rt",str((frame/20)-segment["time"])).replace("t",str(frame/20)))

def getCurrentSegment():
    global on

    sec = frame/20
    lastSeg = None

    on = 0
    for seg in show:
        if sec < seg["time"]: return lastSeg
        if seg == show[-1]:
            on += 1
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

while running:
    frame += 1
    time.sleep(.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    segment = getCurrentSegment()
    drawPixels(func=cfunction)

    drawText(screen, font, f"{on-1}", (0,0,0), (255,255,255), (5,0))                                   # Segment on
    drawText(screen, fontsmall, f"{frame}", (0,0,0), (255,255,255), (5,60), outlineSize=1)             # Frame on
    drawText(screen, fontsmall, f"{frame/20}s", (0,0,0), (255,255,255), (5,80), outlineSize=1)         # Time

    pygame.display.flip()

pygame.quit()