from graphics import *
import random
import time


class Dot(Circle):
    def __init__(self, location, velocity):
        Circle.__init__(self, location, 2)
        self.velocity = velocity

window = GraphWin("Circles", 1920, 990)
borderSize = 100

dots = []
numberOfDots=45
maxSpeed = 250

lines = []
threshold = 150
ratio = 1/3

lastFrameTime = 0

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
                    checkedLines = []
                    p1 = dot.getCenter()
                    p2 = otherDot.getCenter()
                    distance = p1.findDistance(p2)
                    if (distance < threshold):
                        l = Line(dot.getCenter(), otherDot.getCenter())
                        lines.append(l)
                        l.draw(window)

                        l.setFill("gray")
                        if (distance < threshold * ratio):
                            l.setFill("white")
                            if (distance < threshold * ratio * ratio):
                                l.setFill("blue")

                        for otherLine in lines:
                            if otherLine not in checkedLines:
                                if l != otherLine and not l.commonEndpoints(otherLine):
                                    if (otherLine.intersectLine(l, window)):
                                        l.undraw()
                                checkedLines.append(otherLine)
                            checkedLines.append(l)
                        drawnDots.append(dot)
    global lastFrameTime 
    lastFrameTime = time.time() - lastTime
    #print("done updating dots: took", lastFrameTime)

def UpdateSingleDot(dot):
    dot.move(dot.velocity.x * lastFrameTime, dot.velocity.y * lastFrameTime)
    if (borderSize > dot.getCenter().x or dot.getCenter().x > window.width-borderSize or borderSize > dot.getCenter().y or dot.getCenter().y > window.height-borderSize):
        dot.velocity.scale(-1)

def __main__():
    window.autoflush = 0
    window.setBackground("black")


    i = 0
    while i < numberOfDots:
        dots.append(Dot(GetRandomVector(borderSize*2, window.width-borderSize*2, borderSize*2, window.height-borderSize*2), GetRandomVector(maxSpeed*-1,maxSpeed, maxSpeed*-1,maxSpeed)))
        i += 1

    while (window.isOpen):
        lastTime = time.time()
        UpdateDots(dots, lastTime)
        window.update()

    exit()

__main__()
