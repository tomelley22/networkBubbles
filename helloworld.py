from graphics import *
import random
import threading
import time


class Dot(Circle):
    def __init__(self, location, velocity):
        Circle.__init__(self, location, 10)
        self.velocity = velocity

window = GraphWin("Circles", 1000, 1000)
borderSize = 50

dots = []
maxSpeed = 20

lines = []

lastFrameTime = 0;

def GetRandomVector(minX, maxX, minY, maxY):
    return Vector(random.randint(minX,maxX), random.randint(minY,maxY))

def UpdateDots(dots, lastTime):
    for l in lines:
        l.undraw()
    lines.clear()

    for dot in dots:
        UpdateSingleDot(dot)

    drawnDots = []
    for dot in dots:
        if dot not in drawnDots:
            for otherDot in dots:
                if otherDot not in drawnDots:
                    distance = dot.getCenter().findDistance(otherDot.getCenter())
                    if (distance < 100):
                        l = Line(dot.getCenter(), otherDot.getCenter())
                        l.setFill("blue")
                        l.draw(window)
                        lines.append(l)
                        drawnDots.append(dot)
    global lastFrameTime 
    lastFrameTime = time.time() - lastTime
    print("done updating dots: took", lastFrameTime)

def UpdateSingleDot(dot):
    dot.move(dot.velocity.x * lastFrameTime, dot.velocity.y * lastFrameTime)
    if (borderSize > dot.getCenter().x or dot.getCenter().x > window.width-borderSize or borderSize > dot.getCenter().y or dot.getCenter().y > window.width-borderSize):
        dot.velocity.scale(-1)

def __main__():
    window.autoflush = 0


    i = 1
    while i < 100:
        dots.append(Dot(GetRandomVector(borderSize, window.width-borderSize, borderSize, window.height-borderSize), GetRandomVector(maxSpeed*-1,maxSpeed, maxSpeed*-1,maxSpeed)))
        i += 1

    for _ in dots:
        _.draw(window)

    while (window.isOpen):
        lastTime = time.time()
        UpdateDots(dots, lastTime)
        window.update()

    exit()

__main__()