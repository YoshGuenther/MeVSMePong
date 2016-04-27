'''
Created on Mar 23, 2015
@author: JGuenther

Modified on April 14, 2015
@author: DKolinko
@author: LMoyer
'''
import pygame, sys
from pygame.locals import *
# from Carbon.Fonts import courier

# Class to Handle User Interface
class GameMenu():
    def __init__(self, display):
        self.playing = False
        self.do_display = True
        self.useANN = False
        self.useANNvUSER = False
        self.gameScreen = display
        self.options = []
        screenWidth = self.gameScreen.get_width()
        width = 400
        # height = 500
        # margin = 15
        x = int(screenWidth / 2) - int(width / 2)
        # y = int(self.gameScreen.get_height()/2)
        # self.options.append(Option(x, 0, width, 275, " ", (245, 245, 245)))
        self.options.append(Option(x, 0, width, 40, " ", (245, 245, 152)))
        self.options.append(Option(x, 40, width, 70, " ", (232, 215, 0)))
        self.options.append(Option(x, 110, width, 95, " ", (156, 200, 61)))
        self.options.append(Option(x, 205, width, 25, " ", (105, 173, 81)))
        self.options.append(OptionB(x, 230, width, 30, "                     COLOR  PONG", (105, 173, 81)))
        self.options.append(Option(x, 260, width, 20, "                                   Begin User Game", (105, 173, 81)))
        self.options.append(Option(x, 280, width, 20,  "                                      Begin AI Game", (105, 173, 81)))
        self.options.append(Option(x, 300, width, 35, "                              Begin AI vs. User Game", (105, 173, 81)))
        self.options.append(Option(x, 335, width, 200, " ", (76, 138, 131)))
    def render(self, gameScreen):
        for o in self.options:
            o.render(gameScreen)

    # handle events
    # If you fail to make a call to the event queue for too long, the system may decide your program has locked up.
    def handleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            for o in self.options:
                if o.collide(mousePos[0], mousePos[1]):
                    if o.text == "                                   Begin User Game":
                        self.playing = True
                        self.do_display = True
                        self.useANN = False
                    elif o.text == "                                      Begin AI Game":
                        print "ai vs ai"
                        self.playing = True
                        self.do_display = False
                        self.useANN = True
                    elif o.text == "                              Begin AI vs. User Game":
                        print "ai vs user"
                        self.playing = True
                        self.do_display = False
                        self.useANN = False
                        self.useANNvUSER = True
                    else:
                        print "unknown button selected from menu: " + str(o)




class Option(object):
    def __init__(self, x, y, w, h, text, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.fontColor = (245, 245, 152)

    def render(self, gameScreen):
        # Draw Background Shape
        rectangle = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(gameScreen, self.color, rectangle)
        # Draw Text
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.text), 1, self.fontColor)
        gameScreen.blit(text, (self.x, self.y))


    def collide(self, x, y):
        leftXBound = self.x < x
        rightXBound = self.x + self.w > x
        bottomYBound = self.y < y
        topYBound = self.y + self.h > y
        results = leftXBound and rightXBound and bottomYBound and topYBound
        return results

class OptionB(object):
    def __init__(self, x, y, w, h, text, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.fontColor = (245, 245, 152)

    def render(self, gameScreen):
        # Draw Background Shape
        rectangle = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(gameScreen, self.color, rectangle)
        # Draw Text
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.text), 1, self.fontColor)
        gameScreen.blit(text, (self.x, self.y))


    def collide(self, x, y):
        leftXBound = self.x < x
        rightXBound = self.x + self.w > x
        bottomYBound = self.y < y
        topYBound = self.y + self.h > y
        results = leftXBound and rightXBound and bottomYBound and topYBound
        return results
