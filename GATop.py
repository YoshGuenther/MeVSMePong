'''
Created on Mar 28, 2015
@author: JGuenther

Modified on April 14, 2015
@author: DKolinko
@author: LMoyer
'''

from ANN import *
import random
import pygame,sys
from pygame.locals import *

#Class representing a Genetic Algorithm
class GA():
    def __init__(self, display, annVuser = None):
        if annVuser is None:
            self.useANNvUSER = False
        else:
            self.useANNvUSER = True
        self.gameScreen = display
        self.pop_size =5
        self.generations =1
        self.curGeneration = 0
        self.populationTop = []
        self.populationBottom = []
        for x in range(self.pop_size):
            self.populationTop.append(ANN())
            self.populationBottom.append(ANN())

    def runGA(self):
        best = None
        self.curGeneration = 1
        #Run for the number of generations specified
        while self.curGeneration <= self.generations:
            self.render()
            #Calculate the fitness (play the game)
            count = 0
            for t, b in zip(self.populationTop, self.populationBottom):
                print "Evaulating individual: "+str(count)+" ANN is: "+str(t) + " and " + str(b)
                count += 1
                ann = []
                ann.append(t)
                ann.append(b)
                self.evaluateANN(ann)


            #Compare fitness - Determine best and population to keep
            self.selectionSort(self.populationTop)
            self.selectionSort(self.populationBottom)
            best = []
            best.append(self.populationTop[len(self.populationTop)-1])
            best.append(self.populationBottom[len(self.populationBottom)-1])
            self.populationTop = self.populationTop[self.pop_size/2 : len(self.populationTop)] #keep top 50% of population, discard the rest
            self.populationBottom = self.populationBottom[self.pop_size/2 : len(self.populationBottom)]

            new_populationTop = [best[0]]
            new_populationBottom = [best[1]]
            #Perform Variation (Mutation/CrossOver)
            for x in range(1, self.pop_size):
                if random.random() < 0.5:   # randomly pick a member of population, mutate, and add to new pop
                    childTop = random.choice(self.populationTop).mutate()
                    childBottom = random.choice(self.populationBottom).mutate()
                    new_populationTop.append(childTop)
                    new_populationBottom.append(childBottom)
                else: #pick two random parents, perform crossover, and add child to population
                    p1 = random.choice(self.populationTop)
                    p2 = random.choice(self.populationTop)
                    p3 = random.choice(self.populationBottom)
                    p4 = random.choice(self.populationBottom)
                    childTop = p1.crossover(p3)
                    new_populationTop.append(childTop)
                    childBottom = p2.crossover(p4)
                    new_populationTop.append(childBottom)
            #update population with the new children
            self.populationTop = new_populationTop
            self.populationBottom = new_populationBottom
            self.curGeneration += 1
            print "Best ANN is: "+str(best[0]) + " and " + str(best[1])
        #After completing every generation, return the best
        return best


    def evaluateANN(self, ann):
        if self.useANNvUSER is False:
            game = GameManager(self.gameScreen, True, ann)
        else:
            game = GameManager(self.gameScreen, True, ann, True)
        game.gameLoop()
        annTop = ann[0]
        annBottom = ann[1]
        annTop.fitness = game.scoreTop
        annBottom.fitness = game.scoreBottom
        game = None

    def selectionSort(self, array):
        for i  in range(len(array)-1):
            index = i
            for b in range(i+1, len(array)):
                if array[index] > array[b]:
                    index = b
            temp = array[i]
            array[i] = array[index]
            array[index] = temp

    def render(self):
        gameScreen = self.gameScreen
        gameScreen.fill((57, 92, 142))
        fontSize = 20
        font = pygame.font.Font(None, fontSize)
        x = int(gameScreen.get_width()/2) - 40
        y = int(gameScreen.get_height()/2)
        output = ["Running GA", "Generation: "+str(self.curGeneration)+"/"+str(self.generations), "Population Size: "+str(self.pop_size), "Best Fitness: "+str(self.populationTop[0].fitness)]
        for s in range(len(output)):
            text = font.render(output[s], 1, (245,245,245))
            gameScreen.blit(text, (x, y + (s * fontSize)))
        pygame.display.update()
