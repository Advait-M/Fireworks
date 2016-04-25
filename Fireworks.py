#!/usr/bin/env python
"""This program animates fireworks exploding in the sky."""
#Programmer: Advait Maybhate
#Last modified: Nov. 10, 2015


#IMPORT MODULES
from tkinter import *
import time
import math
import random
import winsound

########## EDITABLE VARIABLES ##########
numFireworks = 35 #Number of fireworks
personNum = 8 #Number of people
minXV = 15 #Minimum horizontal velocity for fireworks
maxXV = 25 #Maximum horizontal velocity for fireworks
minYV = 75 #Minimum vertical velocity for fireworks
maxYV = 110 #Maximum vertical velocity for fireworks
minR = 5 #Minimum radius for fireworks
maxR = 15 #Maximum radius for fireworks



########## CORE PROGRAM ##########

# INITIALIZE TKINTER
myInterface = Tk()
s = Canvas(myInterface, width=800, height=800, background="black")
s.pack()

# IMPORT SOUND AND PICTURE FILES
fireworksSound = "Firework sound.wav"
crowdSound = "Crowd sound.wav"
person = PhotoImage(file = "person.gif")

# MAKE GRID OVERLAY (only enable if developing)
gridOverlay = False
if gridOverlay:
    spacing = 50
    for x in range(0, 800, spacing): 
        s.create_line(x, 10, x, 800, fill="black")
        s.create_text(x, 0, text=str(x), font="Times 8", anchor = N)

    for y in range(0, 800, spacing):
        s.create_line(20, y, 800, y, fill="black")
        s.create_text(4, y, text=str(y), font="Times 8", anchor = W)

def cloud(x, y, col):
    """Create a cloud on the screen"""
    s.create_oval(125+x, 50+y, 175+x, 100+y, fill = col, outline = col)
    s.create_oval(100+x, 75+y, 150+x, 125+y, fill = col, outline = col)
    s.create_oval(125+x, 100+y, 175+x, 150+y, fill = col, outline = col)
    s.create_oval(150+x, 50+y, 200+x, 100+y, fill = col, outline = col)
    s.create_oval(150+x, 100+y, 200+x, 150+y, fill = col, outline = col)
    s.create_oval(175+x, 75+y, 225+x, 125+y, fill = col, outline = col)
    s.create_oval(125+x, 75+y, 200+x, 125+y, fill = col, outline = col)

# BUILDING FUNCTION (creates a building)
# bcol = building colour wcol = window colour
# wheight = window height wwidth = window width
# steph = spacing between windows (vertical) stepw = spacing between windows (horizontal)
def building(x1, y1, x2, y2, bcol, wcol, wheight, wwidth, steph, stepw):
    """Create a building at coordinates x1, y1, x2, y2
    bcol -- building colour
    wcol -- window colour
    wheight -- window height
    wwidth -- window width
    steph -- spacing between windows (vertical)
    stepw -- spacing between windows (horizontal)
    """
    s.create_rectangle(x1, y1, x2, y2, fill = bcol)
    for e in range(y1 + 5, y2 - 10, steph):
        for f in range(x1 + 5, x2 - 10, stepw):
            s.create_rectangle(f, e, f + wwidth, e + wheight, fill = wcol)

# HEXADECIMAL FUNCTION - creates a random string that is a hexadecimal value 
def hexadecimal():
    hexadecimals = "#"
    for i in range(0, 6):
        a = random.randint(48, 70)
        while 58 <= a <= 64:
            a = random.randint(48,70)
        hexadecimals += chr(a)
    # Try-Except block makes sure colour is not too dark
    try:
        if int(hexadecimals[1]) < 3 and int(hexadecimals[3]) < 3 and int(hexadecimals[5]) < 3:
            return hexadecimal()
    except ValueError:
        #ValueError - Can happen if trying to turn a letter to an integer
        pass
    return hexadecimals

# DRAW BACKGROUND (uses cloud and building functions)
cloud(0, 0, "white")
cloud(100, 100, "white")
cloud(250, 10, "white")
cloud(400, 150, "white")
cloud(500, 25, "white")
building(300, 250, 400, 700, "purple", "yellow", 10, 7, 20, 20)
building(500, 400, 550, 700, "green", "yellow", 7, 10, 20, 15)
building(600, 350, 700, 700, "light blue", "yellow", 10, 10, 15, 20)
building(150, 200, 200, 700, "brown", "yellow", 7, 10, 20, 15)

# RUN ANIMATION INFINITELY
while True:
    #Initialize variables related to fireworks
    counterA = False
    counterB = False
    xStart = []
    yStart = []
    x = []
    y = []
    vix = []
    viy = []
    firework = []
    fireworkColours = []
    particlesAmount = []
    ft = []
    finalX = []
    m = []
    radii = []

    #Initialize variables related to the particles
    xP = []
    yP = []
    particles = []
    angles = []
    xSizes = []
    ySizes = []
    r = []
    rSpeeds = []
    counter = []
    fCur = []
    stayInSkyFrames = []

    #Initialize variables related to the crowd
    crowd = []
    xCrowd = []
    yCrowd = []
    ySpeedCrowd = []
    
    #Fill the crowd variables
    for h in range(0, personNum):
        crowd.append(0)
        xCrowd.append(h*(800/personNum) + 50)
        yCrowd.append(800)
        ySpeedCrowd.append(random.randint(2, 5))
        
    #Fill the firework variables
    for fireworkNum in range(0, numFireworks):
        radii.append(random.randint(minR, maxR))
        finalX.append(0)
        firework.append(0)
        m.append(0)
        ft.append(0)
        x.append(0)
        y.append(0)
        xStart.append(random.randint(100, 700))
        yStart.append(random.randint(600, 700))
        vix.append(random.randint(minXV, maxXV))
        viy.append(random.randint(minYV, maxYV))
        fireworkColours.append(hexadecimal())
        
        #Fill the particle variables
        #(Use temporary lists that will be appended onto the main list later in order to have nested lists)
        rTemp = []
        xSizesTemp = []
        ySizesTemp = []
        rSpeedsTemp = []
        particlesTemp = []
        anglesTemp = []
        xPTemp = []
        yPTemp = []
        counter.append(True)
        fCur.append(0)
        stayInSkyFrames.append(radii[fireworkNum] * 3)

        #Loop through number of particles and fill temporary lists (number of particles depends of size of firework - radius * 10)
        #Speed of particles depends on size of firework (randint between negative and postive value of radius since bigger fireworks have faster particles
        for particleNum in range(0, radii[fireworkNum] * 10):
            xPTemp.append(0)
            yPTemp.append(0)
            dAngle = random.randint(1, 360)
            rAngle = math.radians(dAngle)
            anglesTemp.append(rAngle)
            rTemp.append(random.randint(-15, 15))
            xSizesTemp.append(random.randint(3, 7))
            ySizesTemp.append(random.randint(3, 7))
            rSpeedsTemp.append(random.randint(-radii[fireworkNum], radii[fireworkNum]))
            while rSpeedsTemp[particleNum] == 0:
                rSpeedsTemp[particleNum] = random.randint(-15, 15)
            particlesTemp.append(0)

        #Append temporary lists to main lists
        r.append(rTemp)
        xSizes.append(xSizesTemp)
        ySizes.append(ySizesTemp)
        rSpeeds.append(rSpeedsTemp)
        particles.append(particlesTemp)
        angles.append(anglesTemp)
        xP.append(xPTemp)
        yP.append(yPTemp)

    #Play initial cheering sound
    winsound.PlaySound(crowdSound, winsound.SND_FILENAME| winsound.SND_ASYNC)     

    #Play animation for 500 frames
    for f in range(0, 500):
        #Play explosion and clapping sound after first explosion
        if counterA and counterB:
            counterB = False
            winsound.PlaySound(fireworksSound, winsound.SND_FILENAME| winsound.SND_ASYNC)

        #Animate crowd
        for h in range(0, personNum):
                yCrowd[h] = yCrowd[h] - ySpeedCrowd[h]
                while yCrowd[h] <= 780:
                    yCrowd[h]  = random.randint(790, 800)
                crowd[h] = s.create_image(xCrowd[h], yCrowd[h], image = person)

        #Animate fireworks
        for i in range(0, numFireworks):
            #Use velocity formulas to find x and y values of the fireworks
            ft[i] = -2 * viy[i] / -9.8
            finalX[i] = vix[i] * ft[i]
            m[i] += 1
            
            #If at the peak of the parabola (technically minimum since tkinter y values are upside down)
            #start explosions
            if m[i] >= finalX[i]/2:
                #Change counters (counters give info on whether a specific event has happened)
                if not counterA:
                    counterA = True
                    counterB = True
                if counter[i]:
                    fCur[i] = f
                    counter[i] = False

                #Animate particles
                for q in range(0, radii[i] * 10):
                    #Calculate x and y values of each particle
                    xP[i][q] = x[i] + r[i][q] * math.cos(angles[i][q])
                    yP[i][q] = y[i] - r[i][q] * math.sin(angles[i][q])
                    r[i][q] = r[i][q] + rSpeeds[i][q]
                    
                    #Create a rectangle or oval representing the particle
                    if q % 2 == 0 and f - fCur[i] < stayInSkyFrames[i]:
                        particles[i][q] = s.create_oval(xP[i][q], yP[i][q], xP[i][q] + xSizes[i][q], yP[i][q] + ySizes[i][q], fill = fireworkColours[i])
                    elif f - fCur[i] < stayInSkyFrames[i]:
                        particles[i][q] = s.create_rectangle(xP[i][q], yP[i][q], xP[i][q] + xSizes[i][q], yP[i][q] + ySizes[i][q], fill = fireworkColours[i])
            #If not at peak of parabola then animate fireworks
            else:
                #Calculate current time (in terms of the parabola)
                t = ft[i]/finalX[i] * m[i]
                #Either have the parabola go from left to right or right to left
                if i % 2 == 0:
                    x[i] = vix[i] * t + xStart[i]
                else:
                    x[i] = xStart[i] - vix[i] * t
                #Calculate y value (velocity formula)
                y[i] = -1*(viy[i] * t + 0.5*-9.8*t**2) + yStart[i]
                #Create firework
                firework[i] = s.create_oval(x[i] - radii[i], y[i] - radii[i], x[i]+ radii[i], y[i]+radii[i], fill = fireworkColours[i])

        #Update screen and sleep (so user can watch animation)
        s.update()
        time.sleep(0.02)
        
        #Delete fireworks (for animation effect)
        for d in range(0, numFireworks):
            s.delete(firework[d])
            #Delete particles (for animation effect)
            for q in range(0, radii[d] * 10):
                s.delete(particles[d][q])
                
        #Delete crowd (for animation effect)
        for k in range(0, personNum):
            s.delete(crowd[k])        
