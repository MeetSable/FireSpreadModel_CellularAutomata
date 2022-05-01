from tkinter import font

from matplotlib.pyplot import text
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

sideBar = 500
font = pygame.font.Font('./font.ttf', 32)

class Simulator():

    def __init__(self) -> None:
        self.backgroundColor = BLACK
        self.n = 100
        self.cellSize = 5
        self.windowWidth = self.n * self.cellSize
        self.screen = pygame.display.set_mode((self.windowWidth + sideBar, self.windowWidth ))
        self.running = True
        self.frame = 0
        self.play = False
        self.fps = float(10)
        self.playBackSpeed = float(1/self.fps)
        self.start = time.time()
        self.fireModel = FireSpreadModel(self.n, 0.8, 0.001, 0.00, 0.3, 0, 'random', 'simple', wind=True, windDir='N',windLevel=1, varyDirection=True)
        self.fireModel.run()
        self.frameMax = self.fireModel.time

    
    def run(self):
        while self.running:
            self.event()
            self.Update()
            self.Render()

    def Render(self):
        self.drawGrid()
        self.Text('t = {}  (t_max = {})'.format(self.frame, self.frameMax), 0)
        self.Text('Speed: {}'.format(self.fps), 1)

        if self.play:
            self.Text('state: play', 2)
        else:
            self.Text('state: pause', 2)
        
        if self.fireModel.wind:
            if(self.fireModel.windDirArr[self.frame] == 'N'):
                self.Text('Wind: N (Up)', 3)
            elif(self.fireModel.windDirArr[self.frame] == 'S'):
                self.Text('Wind: S (Down)', 3)
            elif(self.fireModel.windDirArr[self.frame] == 'E'):
                self.Text('Wind: E (Right)', 3)
            elif(self.fireModel.windDirArr[self.frame] == 'W'):
                self.Text('Wind: W (Left)', 3)
        else:
            self.Text('Wind: None', 3)
        pygame.display.update()
        self.screen.fill(self.backgroundColor)
    
    def Update(self):
        if(self.play & (time.time()-self.start >= self.playBackSpeed)):
            self.start = time.time()
            self.frame = min(self.frame + 1, self.frameMax-1)
            if self.frame == self.frameMax-1:
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
                if event.key == pygame.K_p:
                    self.fps += 1
                    self.fps = min(self.fps, 60)
                    self.playBackSpeed = 1/self.fps
                if event.key == pygame.K_o:
                    self.fps -= 1
                    self.fps = max(self.fps, 1)
                    self.playBackSpeed = 1/self.fps
                if event.key == pygame.K_r:
                    self.frame = 0
            if event.type == pygame.QUIT:
                self.running = False
    
    def Text(self, tex, line):
        text = font.render(tex, True, WHITE)
        textRect = text.get_rect()
        textRect.x = self.windowWidth + 5
        textRect.y += line*textRect.height
        self.screen.blit(text, textRect)

    def drawGrid(self):
        for i in range(self.fireModel.n):
            for j in range(self.fireModel.n):
                rect = pygame.Rect(i*self.cellSize, j*self.cellSize, self.cellSize, self.cellSize)
                currentCellState = self.fireModel.grids[self.frame][i][j]
                if (currentCellState == 0):
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif (currentCellState == 1):
                    pygame.draw.rect(self.screen, TREE, rect)
                elif (currentCellState >= 2):
                    pygame.draw.rect(self.screen, BURNING, rect)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0, 0, self.windowWidth,self.windowWidth),1)


sim = Simulator()
sim.run()
