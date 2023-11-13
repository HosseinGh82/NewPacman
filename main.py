# <editor-fold desc="Imports">
import math
import random
from time import sleep
import os


# </editor-fold>


# <editor-fold desc="Classes">
class Game:
    def __init__(self, mapG, pac, gh1, gh2, scb, sc):
        self.pacman = pac
        self.ghost1 = gh1
        self.ghost2 = gh2
        self.scoreBoard = scb
        self.score = sc
        self.mapGame = mapG

    def printGame(self):
        print("Score: %d" % self.scoreBoard)
        for i in range(self.mapGame.height):
            for j in range(self.mapGame.width):
                if i == self.ghost1.x and j == self.ghost1.y or i == self.ghost2.x and j == self.ghost2.y:
                    if i == self.ghost1.x and j == self.ghost1.y:
                        print("G", end=" ")
                    else:
                        print("g", end=" ")
                elif i == self.pacman.x and j == self.pacman.y:
                    print("P", end=" ")
                else:
                    print(self.mapGame.array[i][j], end=" ")
            print("")


class Pacman:
    def __init__(self, locX, locY):
        self.x = locX
        self.y = locY

    def printPackmanSituation(self):
        print("Pacman location: (%d, %d)" % (self.x, self.y))


class Ghost:
    def __init__(self, locX, locY):
        self.x = locX
        self.y = locY

    def printGhostSituation(self):
        print("Ghost location: (%d, %d)" % (self.x, self.y))


class Map:
    def __init__(self, h, w, arr):
        self.height = h
        self.width = w
        self.array = arr

    def fillMap(self):
        self.array = [["#" if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1
                       else " " for j in range(self.width)] for i in range(self.height)]

        self.array[1][1] = "+"

        # <editor-fold desc="Collision in map">
        self.array[1][5] = '#'
        self.array[1][14] = '#'
        self.array[2][2] = '#'
        self.array[2][3] = '#'
        self.array[2][5] = '#'
        self.array[2][7] = '#'
        self.array[2][8] = '#'
        self.array[2][9] = '#'
        self.array[2][10] = '#'
        self.array[2][11] = '#'
        self.array[2][12] = '#'
        self.array[2][14] = '#'
        self.array[2][16] = '#'
        self.array[2][17] = '#'
        self.array[3][2] = '#'
        self.array[3][17] = '#'
        self.array[4][2] = '#'
        self.array[4][4] = '#'
        self.array[4][5] = '#'
        self.array[4][7] = '#'
        self.array[4][8] = '#'
        self.array[4][11] = '#'
        self.array[4][12] = '#'
        self.array[4][14] = '#'
        self.array[4][15] = '#'
        self.array[4][17] = '#'
        self.array[5][7] = '#'
        self.array[5][12] = '#'
        self.array[9][5] = '#'
        self.array[9][14] = '#'
        self.array[8][2] = '#'
        self.array[8][3] = '#'
        self.array[8][5] = '#'
        self.array[8][7] = '#'
        self.array[8][8] = '#'
        self.array[8][9] = '#'
        self.array[8][10] = '#'
        self.array[8][11] = '#'
        self.array[8][12] = '#'
        self.array[8][14] = '#'
        self.array[8][16] = '#'
        self.array[8][17] = '#'
        self.array[7][2] = '#'
        self.array[7][17] = '#'
        self.array[6][2] = '#'
        self.array[6][4] = '#'
        self.array[6][5] = '#'
        self.array[6][7] = '#'
        self.array[6][8] = '#'
        self.array[6][11] = '#'
        self.array[6][12] = '#'
        self.array[6][14] = '#'
        self.array[6][15] = '#'
        self.array[6][17] = '#'
        self.array[6][9] = '#'
        self.array[6][10] = '#'
        # </editor-fold>

    def printMap(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.array[i][j], end=" ")
            print("")


# </editor-fold>


# <editor-fold desc="Objects">
pacman = Pacman(1, 1)
ghost1 = Ghost(1, 12)
ghost2 = Ghost(1, 13)

height = 11
width = 20
array = [[0] * width] * height
mapGame = Map(height, width, array)
mapGame.fillMap()

game = Game(mapGame, pacman, ghost1, ghost2, 0, 0)


# </editor-fold>


def doesEatAllFoods(gameTemp):
    for i in range(gameTemp.mapGame.height):
        for j in range(gameTemp.mapGame.width):
            if gameTemp.mapGame.array[i][j] == "+":
                return False
    return True


def finishGame(gameTemp):
    if (gameTemp.pacman.x == gameTemp.ghost1.x and gameTemp.pacman.y == gameTemp.ghost1.y) or (
            gameTemp.pacman.x == gameTemp.ghost2.x and gameTemp.pacman.y == gameTemp.ghost2.y):
        return -1
    elif doesEatAllFoods(gameTemp):
        return 1
    else:
        return 0


def ghostMove(gameMapArray, gh):
    direction = {0: "U", 1: "R", 2: "D", 3: "L"}
    while True:
        r = random.randint(0, 3)
        if r == 0 and gameMapArray[gh.x - 1][gh.y] != "#":
            return gh.x - 1, gh.y
        if r == 1 and gameMapArray[gh.x][gh.y + 1] != "#":
            return gh.x, gh.y + 1
        if r == 2 and gameMapArray[gh.x + 1][gh.y] != "#":
            return gh.x + 1, gh.y
        if r == 3 and gameMapArray[gh.x][gh.y - 1] != "#":
            return gh.x, gh.y - 1


def startGame(gameTemp, turn):
    while True:
        gameTemp.printGame()
        if finishGame(gameTemp) == -1:
            print("GAME OVER")
            break
        elif finishGame(gameTemp) == 1:
            print("YOU WIN")
            break

        if turn == 0:
            continue
        if turn == 1:
            gameTemp.ghost1.x, gameTemp.ghost1.y = ghostMove(gameTemp.mapGame.array, gameTemp.ghost1)
            turn = 2
        if turn == 2:
            gameTemp.ghost2.x, gameTemp.ghost2.y = ghostMove(gameTemp.mapGame.array, gameTemp.ghost2)
            turn = 1
        sleep(0.01)
        os.system("cls")


startGame(game, 1)
