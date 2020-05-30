from graphics import GraphWin, Circle, Vector, Line
import random
import time
import sys

global lines
global dots
window = GraphWin("Circles", 500, 500)
borderSize = 20
backgroundColor = "black"

dots = []
dotColor="red"
dotSize = 0
numberOfDots=25
maxSpeed = 200
drawDots = 1

lines = []
threshold = 500
ratio = 1/3

lastFrameTime = 0
desiredFrameTime = 1

class Dot(Circle):
    def __init__(self, location, velocity):
        Circle.__init__(self, location, dotSize)
        self.velocity = velocity
        self.setFill(dotColor)

def GetRandomVector(minX, maxX, minY, maxY):
    return Vector(random.randint(minX,maxX), random.randint(minY,maxY))

def __main__():

    window.autoflush = 0
    window.setBackground(backgroundColor)

    i = 0
    while i < numberOfDots:
        dots.append(Dot(GetRandomVector(borderSize*2, window.width-borderSize*2, borderSize*2, window.height-borderSize*2), GetRandomVector(maxSpeed*-1,maxSpeed, maxSpeed*-1,maxSpeed)))
        i += 1

    if (drawDots):
        for dot in dots:
            dot.draw(window)

    while (window.isOpen):
        lastTime = time.time()
        UpdateDots(dots, lastTime)
        window.update()

    exit()


def CreateLines(dots):
    lines = []
    drawnDots = []
    for dot in dots:
        for otherDot in dots:
            if otherDot is not dot and otherDot not in drawnDots:
                lines.append(Line(dots[0].getCenter(), otherDot.getCenter()))
        drawnDots.append(dot)
        dots.remove(dot)
    dots.extend(drawnDots.copy())
    return lines

def UpdateDots(dots, lastTime):
    global lines
    for l in lines:
        l.undraw()

    for dot in dots:
        UpdateSingleDot(dot)

    lines = CreateLines(dots)

    checkedLines = []
    for l1 in lines:
        if l1.getLength() < threshold:
            for l2 in lines:
                if l1.commonEndpoints(l2):
                    continue
                if l1.intersectLine(l2, 2, window):
                    #print("undrawing line")
                    l1.toBeDrawn = 0
                    l2.toBeDrawn = 0
                    checkedLines.append(l2)
                    lines.remove(l2)
                else:
                    #print("tagging line for draw")
                    l1.toBeDrawn = 1
        checkedLines.append(l1)
        lines.remove(l1)

    lines.extend(checkedLines.copy())

    for l in lines:
        l.setFill("blue")#"white" if l.getLength() > threshold / 2 else "gray")
        if (l.toBeDrawn):
            print("drawing line")
            l.draw(window)
        else:
            l.undraw()

    global lastFrameTime
    lastFrameTime = time.time() - lastTime
    print("done updating dots: took", lastFrameTime)
    if (lastFrameTime < desiredFrameTime):
        time.sleep(desiredFrameTime - lastFrameTime)


def UpdateSingleDot(dot):
    dot.move(dot.velocity.x * desiredFrameTime, dot.velocity.y * desiredFrameTime)
    if (borderSize > dot.getCenter().x or dot.getCenter().x > window.width-borderSize or borderSize > dot.getCenter().y or dot.getCenter().y > window.height-borderSize):
        dot.velocity.scale(-1)

__main__()
