import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import random
from math import *
from matplotlib.widgets import Slider, Button


col_dict = {
    0:"grey",
    1:"green",
    2:"yellow"
}
cm = ListedColormap([col_dict[x] for x in col_dict.keys()])

prec = 1000000

def rand():
    return random.randrange(0,prec,1)/float(prec)


class FireSpreadModel():

    def __init__(self, n, probTree, probBurning, probLightning, probImmune, t, mode) -> None:
        self.n = n
        self.probTree = probTree
        self.probBurning = probBurning
        self.probLightning = probLightning
        self.probImmune = probImmune
        self.t = t
        self.mode = mode
        self.grid = np.array([[0 for i in range(n)] for j in range(n)])

    def initRandomForest(self):
        #init trees
        for i in range(self.n):
            for j in range(self.n):
                p = rand()
                if(p<self.probTree):
                    self.grid[i][j] = 1
        #init fire
        for i in range(self.n):
            for j in range(self.n):
                p = rand()
                if(p<self.probBurning):
                    if(self.grid[i][j] == 1):
                        # print('elo')
                        self.grid[i][j] = 2

    def initAllTree(self):
        for i in range(self.n):
            for j in range(self.n):
                self.grid[i][j] = 1

    def BurningNeighbour(self, x, y, gridPrev):
        if ((gridPrev[(x)%self.n][(y - 1)%self.n] == 2) or (gridPrev[(x)%self.n][(y + 1)%self.n] == 2) or (gridPrev[(x + 1)%self.n][(y)%self.n] == 2) or (gridPrev[(x - 1)%self.n][(y)%self.n] == 2)):
            return True
        return False    

    def ApplyDiffusion(self):     
        gridPrev = self.grid.copy()
        for x in range(self.n):
            for y in range(self.n):
                if gridPrev[x][y] == 1:
                    p = rand()
                    if self.BurningNeighbour(x,y, gridPrev):
                        if(p>self.probImmune):
                            self.grid[x][y]=2
                    elif p < self.probLightning:
                        self.grid[x][y]=2
                        
        for x in range(self.n):
            for y in range(self.n):
                if(gridPrev[x][y] == 2):
                    self.grid[x][y]=0

    def run(self):
        if (self.mode == 'random'):
            self.initRandomForest()
        elif (self.mode == 'center'):
            self.initAllTree()
            self.grid[int(self.n/2)][int(self.n/2)] = 2
            

        self.grids=[np.array(self.grid)]
        for i in range(self.t):
            self.ApplyDiffusion()
            self.grids.append(np.array(self.grid))
        
    def view(self):
        

        fig, ax = plt.subplots(figsize=[5,5])
        plt.subplots_adjust(bottom=0.35)

        ani = plt.imshow(self.grids[0], cmap=cm)

        timeSlider = Slider(plt.axes([0.1,0.9,0.8,0.04]), 'time', 0, self.t, valstep=1)

        def update(val):
            ani.set_data(self.grids[timeSlider.val])

        timeSlider.on_changed(update)
        plt.show()

