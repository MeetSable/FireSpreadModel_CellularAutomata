from tkinter import font
from FireSpreadModel import FireSpreadModel
import pygame
import time
from pygame.locals import *

WHITE = (255,255,255)
GREY = (105,105,105)
BURNING = (255,0,0)
TREE = (0,120,0)
BLACK = (0,0,0)

pygame.init()
pygame.font.init()

topBar = 40
font = pygame.font.Font('./font.ttf', 32)

class Simulator():

    def __init__(self, n, cell) -> None:
        self.backgroundColor = BLACK
        self.windowWidth = n*cell
        self.cellSize = cell
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowWidth + topBar))
        self.running = True
        self.frame = 0
        self.frameMax = 50
        self.play = False
        self.playBackSpeed = 0.5
        self.start = time.time()
        self.fireModel = FireSpreadModel(n, 0.8, 0.01, 0.000001, 0.1, self.frameMax, 'center')
        self.fireModel.run()

    
    def run(self):
        while self.running:
            self.event()
            self.Update()
            self.Render()

    def Render(self):
        self.drawGrid()
        self.showCurrentFrame()
        pygame.display.update()
        self.screen.fill(self.backgroundColor)
    
    def Update(self):
        if(self.play & (time.time()-self.start >= self.playBackSpeed)):
            self.start = time.time()
            self.frame = min(self.frame + 1, self.frameMax)
            if self.frame == self.frameMax:
                self.play = ~self.play

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.frame = max(self.frame - 1, 0)
                if event.key == pygame.K_RIGHT:
                    self.frame = min(self.frame + 1, self.frameMax)
                if event.key == pygame.K_SPACE:
                    self.start = time.time()
                    self.play = ~self.play
            if event.type == pygame.QUIT:
                self.running = False

    def showCurrentFrame(self):
        self.text = font.render('t = {}'.format(self.frame), True, WHITE)
        self.textRect = self.text.get_rect()
        self.screen.blit(self.text,self.textRect)

    def drawGrid(self):
        for i in range(self.fireModel.n):
            for j in range(self.fireModel.n):
                rect = pygame.Rect(i*self.cellSize, j*self.cellSize + topBar, self.cellSize, self.cellSize)
                currentCellState = self.fireModel.grids[self.frame][i][j]
                if (currentCellState == 0):
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif (currentCellState == 1):
                    pygame.draw.rect(self.screen, TREE, rect)
                elif (currentCellState == 2):
                    pygame.draw.rect(self.screen, BURNING, rect)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0,topBar,self.windowWidth,self.windowWidth),1)


sim = Simulator(17, 20)
sim.run()
