from graphics import GraphWin, Circle, Vector, Line
import random
import time
import sys

window = GraphWin("Circles", 500, 500)
borderSize = 20
backgroundColor = "black"

dots = []
dotColor="red"
dotSize = 0
numberOfDots=10
maxSpeed = 500
drawDots = 0

lines = []
threshold = 500
ratio = 1/3

lastFrameTime = 0
desiredFrameTime = .001

class Dot(Circle):
    def __init__(self, location, velocity):
        Circle.__init__(self, location, dotSize)
        self.velocity = velocity
        self.setFill(dotColor)

def GetRandomVector(minX, maxX, minY, maxY):
    return Vector(random.randint(minX,maxX), random.randint(minY,maxY))

def UpdateDots(dots, lastTime):
    global lines
    for l in lines:
        l.undraw()
    lines = []

    for dot in dots:
        UpdateSingleDot(dot)

    drawnDots = []
    for dot in dots:
        if dot not in drawnDots:
            for otherDot in dots:
                if otherDot not in drawnDots and otherDot is not dot:
                    p1 = dot.getCenter()
                    p2 = otherDot.getCenter()
                    distance = p1.findDistance(p2)
                    if (distance < threshold):
                        l = Line(dot.getCenter(), otherDot.getCenter())
                        drawLine = 1
                        l.setFill("gray")
                        if (distance < threshold * ratio):
                            l.setFill("white")
                            if (distance < threshold * ratio * ratio):
                                l.setFill("blue")
                        for otherLine in lines:
                            if not l.commonEndpoints(otherLine):
                                if (otherLine.intersectLine(l, 3, window)):
                                    drawLine = 0
                        if (drawLine):
                            l.draw(window)
                            lines.append(l)
                        else:
                            l.undraw()
            drawnDots.append(dot)
    global lastFrameTime
    lastFrameTime = time.time() - lastTime
    print("done updating dots: took", lastFrameTime)
    if (lastFrameTime < desiredFrameTime):
        time.sleep(desiredFrameTime - lastFrameTime)

def UpdateSingleDot(dot):
    dot.move(dot.velocity.x * desiredFrameTime, dot.velocity.y * desiredFrameTime)
    if (borderSize > dot.getCenter().x or dot.getCenter().x > window.width-borderSize or borderSize > dot.getCenter().y or dot.getCenter().y > window.height-borderSize):
        dot.velocity.scale(-1)

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

__main__()
