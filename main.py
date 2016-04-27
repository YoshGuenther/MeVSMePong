'''
Created on Mar 12, 2015
@author: JGuenther

Modified on April 14, 2015
@author: DKolinko
@author: LMoyer
'''
import pygame,sys
from pygame.locals import *
import random
from Menu import *
#import math
from GameObjects import *
from GATop import *
#from Carbon.Fonts import times

#Class to run MeVsMePong!
class Main:
    def __init__(self, ann=None):
        pygame.init()
        #run game at 30 frames per second
        self.FPS = 60
        self.FPSCLOCK = pygame.time.Clock()
        #set up display
        self.display = pygame.display.set_mode((400, 500),0,32)
        self.do_display = True
        # initialize font: must be called after 'pygame.init()'
        self.myfont = pygame.font.SysFont("monospace", 30)
        self.menu = GameMenu(self.display)

        #game vars
        self.running = True
        self.playing = False
        self.score = 0

        #game objects
#        self.gameManager = None
#        if ann == None:
#            self.useANN = False;
#            self.ann = None
#        else:
#            self.useANN = True;
#            self.ann = ann

        self.getTicksLastFrame = pygame.time.get_ticks()
        self.deltaTime = 0
        #start the game
        self.gameLoop()

    #Game loop
    def gameLoop(self):
        while self.running == True:
            self.handleEvents("Title")
            self.render("Title")
            self.gameManager = None
            if self.playing == True:
                self.menu.playing = False
                print "-----------------------begin game-----------------------"
                if self.useANN:
                    self.render("GA")
                    ga = GA(self.display)
                    self.ann  = ga.runGA()
                    self.gameManager = GameManager(self.display, True, self.ann)
                elif self.useANNvUSER:
                    self.render("GA")
                    ga = GA(self.display, True)
                    self.ann  = ga.runGA()
                    self.gameManager = GameManager(self.display, True, self.ann, True)
                else:
                    self.gameManager = GameManager(self.display, self.do_display)
                self.playing = self.gameManager.gameLoop()
                self.score = self.gameManager.score
                self.scoreTop = self.gameManager.scoreTop
                self.scoreBottom = self.gameManager.scoreBottom
                print "Top Player score was " + str(self.scoreTop)
                print "Bottom Player score was " + str(self.scoreBottom)
                print "The total score was "+str(self.score)
                print "-----------------end game with playing of: "+str(self.playing)+"--------------------"

        #raw_input() # Hack to not have game quit until user input received (hitting enter)
        pygame.quit()
        sys.exit()




    #handle events
    #If you fail to make a call to the event queue for too long, the system may decide your program has locked up.
    def handleEvents(self, scene="Title"):
        keysPressed = pygame.key.get_pressed();
        for event in pygame.event.get():
            if event.type == QUIT:
                self.playing = False
                self.running = False
            elif(scene == "Title"):
                self.menu.handleEvents(event)
                self.playing = self.menu.playing
                self.menu.playing = False
                self.do_display = self.menu.do_display
                self.menu.do_display = True
                self.useANN = self.menu.useANN
                self.menu.useANN = False
                self.useANNvUSER = self.menu.useANNvUSER
                self.menu.useANNvUSER = False
            else:
                print "unknown input: ",event

    def step(self, dt):
        print "main step"

    #display
    def render(self, scene="Title"):
        #clear screen
        gameScreen = self.display
        gameScreen.fill((245, 245, 152))
        if(scene == "Title"):
            self.menu.render(gameScreen)
        pygame.display.update()
        self.FPSCLOCK.tick(self.FPS)

    def setPlaying(self, play):
        self.playing = play

#I like classes cause it prevents the problem of having to define code before calling it
mainGame = Main()
mainGame.menu.setGameObject(mainGame)
