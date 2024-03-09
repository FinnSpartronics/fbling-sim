import pygame, time, json
pygame.init()

screen = pygame.display.set_mode([900, 100])
pygame.display.set_caption("Bling")
font = pygame.font.SysFont('Comic Sans MS', 30)

pixelCount = 50
frame = 0
on = 0
segment = None
running = True

with open('show.json') as f:
    show = json.load(f)["segments"]

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

while running:
    frame += 1
    time.sleep(.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    segment = getCurrentSegment()
    drawPixels(func=cfunction)

    text_surface = font.render(str(on-1), False, (0, 0, 0))
    screen.blit(text_surface, (0, 0))

    pygame.display.flip()

pygame.quit()