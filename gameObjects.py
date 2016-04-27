'''
Created on Mar 12, 2015

@author: JGuenther
'''
import pygame,sys
from pygame.locals import *
import random
import math
from types import NoneType

#Class that handles the actual game
class GameManager():
    def __init__(self, display, do_display=True, ann=None):
        self.gameScreen = display
        self.do_display = do_display

        self.player = Player(display)
        self.ball = Ball(display)
        self.goal = Goal(display)


        self.getTicksLastFrame = pygame.time.get_ticks()
        self.deltaTime = 0

        self.score = 0
        self.running = True

        if ann is None:
            self.ann = None
            self.useANN = False
        else:
            self.ann = ann
            self.useANN = True

    def gameLoop(self):
        while self.running == True:
            time = pygame.time.get_ticks()

            #check for end of game
            gameState = self.getScore()
            if not gameState[0]:
                self.running = False
                self.score = gameState[1]
            else:
                #Handle input
                if self.useANN:
                    self.annInput(self.ann)
                else:
                    self.playerInput()

                #update logic of game Objects
                self.step(self.deltaTime)

                #update screen via rendering
                if self.do_display and self.gameScreen != None:
                    self.render(self.gameScreen)

            #Calculate deltaTime in seconds.
            self.deltaTime = (time - self.getTicksLastFrame) / 1000.0
            self.getTicksLastFrame = time
        return False

    def playerInput(self):
        #Handle user input
        self.handleEvents("PLAYER")

    def annInput(self, ann):
        self.handleEvents("ANN")
        #Determine input for neural network
        ballMiddleX = self.ball.x + int(self.ball.w/2)
        playerMiddleX = self.player.x+ int(self.player.width/2)
        xDifference = ballMiddleX - playerMiddleX
        sensorInput = [xDifference, self.ball.vx, 1]
        #call neural network
        output = ann.run(sensorInput)
        #handle event
        if(output < 0):
            self.player.setHorizontalMovement(-75)
        elif(output > 0):
            self.player.setHorizontalMovement(75)
        else:
            self.player.setHorizontalMovement(0)

    def step(self, deltaTime):
        if self.running:
            self.ball.step(deltaTime)
            self.player.step(deltaTime)
            ballPaddleCollision = self.player.collide(self.ball.x, self.ball.y, self.ball.w, self.ball.h)
            if ballPaddleCollision[0]:
                #print "Ball-Paddle Collision occured of type: "+str(ballPaddleCollision[1])
                if ballPaddleCollision[1] == "X":
                    self.ball.vx = -self.ball.vx
                elif ballPaddleCollision[1] == "Y":
                    self.ball.vy = -self.ball.vy
                else:
                    print "error with ballPaddleCollision"
                self.score += 1

            ballGoalCollision = self.goal.collide(self.ball.x, self.ball.y, self.ball.w, self.ball.h)
            if ballGoalCollision[0]:
                #print "Ball-Goal Collision occured of type: "+str(ballGoalCollision[1])
                if ballGoalCollision[1] == "X" or ballGoalCollision[1] == "Y":
                    print "Ball Goal collision -- ending game. Score: "+str(self.score)
                    self.running = False
                else:
                    print "error with ballGoalCollision"

    def render(self, gameScreen):
        gameScreen = self.gameScreen
        gameScreen.fill((0, 0, 0))
        if self.do_display:
            self.ball.render(gameScreen)
            self.player.render(gameScreen)
            self.goal.render(gameScreen)

        font = pygame.font.Font(None,15)
        text = font.render("Score: "+str(self.score), 1, (155,155,155))
        gameScreen.blit(text, (10, 10))
        pygame.display.update()

    def getScore(self):
        return [self.running, self.score];

    #handle events
    #If you fail to make a call to the event queue for too long, the system may decide your program has locked up.
    def handleEvents(self, gameMode="PLAYER"):
        keysPressed = pygame.key.get_pressed();
        for event in pygame.event.get():
            if event.type == QUIT or keysPressed[K_ESCAPE]:
                print "quit game"
                self.running = False
        if gameMode == "PLAYER":
                #handle keyboard
                if keysPressed[K_LEFT]:
                    self.player.setHorizontalMovement(-75)
                elif keysPressed[K_RIGHT]:
                    self.player.setHorizontalMovement(75)

                else:
                    self.player.setHorizontalMovement(0)



class Entity(object):
    #define Entities state
    def __init__(self, x, y, w, h, gameScreen, vx, vy,  ax = 3.5, ay = 3.5, color=(244, 244, 244)):
        self.originalStates = [x, y, w, h, vx, vy, ax, ay, color]
        #object coordinates
        self.x = x
        self.y = y
        #object velocity
        self.vx = vx
        self.vy = vy
        self.gameWidth = gameScreen.get_width()
        self.gameHeight = gameScreen.get_height()
        self.ax = ax
        self.ay = ay
        self.w = w
        self.h = h
        self.color = (int(random.random()*255), int(random.random()*255), int(random.random()*255))#color

    def render(self, display):
        pass

    def step(self, deltaTime):
        self.moveHorizontal(deltaTime)
        self.moveVertical(deltaTime)

    def moveHorizontal(self, deltaTime):
        self.vx += self.ax * deltaTime;
        self.x += self.vx * deltaTime;
        #bounce x velocity
        if self.x < 0 or self.x + self.w > self.gameWidth:
            self.vx = -self.vx
            self.ax = -self.ax
        #fix if it goes out of bounds
        if self.x < 0:
            self.x = 1
        elif self.x + self.w > self.gameWidth:
            self.x = self.gameWidth-1-self.w


    def moveVertical(self, deltaTime):
        self.vy += self.ay * deltaTime;
        self.y += self.vy * deltaTime;
        #bounce y velocity
        if self.y < 0 or self.y + self.h > self.gameHeight:
            self.vy = -self.vy
            self.ay = -self.ay
        #fix if it goes out of bounds
        if self.y < 0:
            self.y = 1
        elif self.y + self.h > self.gameHeight:
            self.y = self.gameHeight-1-self.h


    def setVerticalVelocity(self, vy):
        self.vy = vy

    def setColor(self, colorTulip):
        self.color = colorTulip

    def collide(self, x, y, w, h):
        leftXBound = self.x < x+w
        rightXBound = self.x+self.w > x
        bottomYBound = self.y < y+h
        topYBound = self.y+self.h > y
        results = [(leftXBound and rightXBound), (bottomYBound and topYBound)]
        return results

class Ball(Entity):
    def __init__(self, gameScreen):
        super(Ball, self).__init__(int(gameScreen.get_width()/2 - 50), int(gameScreen.get_height()/2 - 50), 25, 25, gameScreen,  50, 50)
        self.setColor((0, 255, 255))

    def render(self, gameScreen):
        self.gameScreen = gameScreen
        rectangle = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(gameScreen, self.color, rectangle)
        super(Ball, self).render(gameScreen)

class Goal:
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.x = 0
        self.topY = 20
        self.bottomY = gameScreen.get_height() - self.topY
        rectOne = Rectangle(self.x, 0, gameScreen, gameScreen.get_width(), self.topY)
        rectOne.setColor((255, 0, 0))
        rectTwo = Rectangle(self.x, self.bottomY, gameScreen, gameScreen.get_width(), self.topY)
        rectTwo.setColor((255, 0, 0))
        self.goals = [rectOne, rectTwo]

    def render(self, gameScreen):
        for g in self.goals:
            g.render(gameScreen)

    def collide(self, x, y, w, h):
        topGoal = self.goals[0].collide(x, y, w, h)
        bottomGoal = self.goals[1].collide(x, y, w, h)
        collision = (bottomGoal[0] and bottomGoal[1]) or (topGoal[0] and topGoal[1])
        type = ""
        if bottomGoal[0] or topGoal[0]:
            type += "Y"
        elif bottomGoal[1] or topGoal[1]:
            type += "X"
        collisionResults = [collision, type]
        return collisionResults

class Player():
    def __init__(self, gameScreen):
        self.gameScreen = gameScreen
        self.x = int(gameScreen.get_width()/2)
        self.width = 100
        self.height = 25
        self.topY = 50
        self.bottomY = gameScreen.get_height()- (self.topY + self.height)

        rectOne = Rectangle(self.x, self.topY, gameScreen, self.width, self.height)
        rectOne.setColor((255, 255, 255))
        rectTwo = Rectangle(self.x, self.bottomY, gameScreen, self.width, self.height)
        rectTwo.setColor((255, 255, 255))
        self.paddles = [rectOne,rectTwo]

    def step(self, deltaTime):
        for p in self.paddles:
            p.moveHorizontal(deltaTime)
        self.x = self.paddles[0].x

    def render(self, gameScreen):
        for p in self.paddles:
            p.render(gameScreen)

    def setHorizontalMovement(self, speed):
        for p in self.paddles:
            p.vx = speed

    def collide(self, x, y, w, h):
        topPaddle = self.paddles[0].collide(x, y, w, h)
        bottomPaddle = self.paddles[1].collide(x, y, w, h)
        collision = (bottomPaddle[0] and bottomPaddle[1]) or (topPaddle[0] and topPaddle[1])
        type = ""
        if bottomPaddle[0] or topPaddle[0]:
            type += "Y"
        elif bottomPaddle[1] or topPaddle[1]:
            type += "X"
        collisionResults = [collision, type]
        return collisionResults


class Rectangle(Entity):
    def __init__(self, x, y, gameScreen, w=100, h=10):
        super(Rectangle, self).__init__(x, y, w, h, gameScreen, 3.5, 3.5)

    def render(self, gameScreen):
        self.gameScreen = gameScreen
        rectangle = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(gameScreen, self.color, rectangle)
        super(Rectangle, self).render(gameScreen)


    def moveHorizontal(self, deltaTime):
        #self.vx += self.ax * deltaTime;
        self.x += self.vx * deltaTime;
        if self.x < 0:
            self.x = 1
        elif self.x + self.w > self.gameWidth:
            self.x = self.gameWidth-self.w-1
