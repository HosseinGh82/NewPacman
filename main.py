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

    def doesEatAllFoods(self):
        for i in range(self.mapGame.height):
            for j in range(self.mapGame.width):
                if self.mapGame.array[i][j] == "+":
                    return False
        return True

    def finishGame(self):
        if (self.pacman.x == self.ghost1.x and self.pacman.y == self.ghost1.y) or (
                self.pacman.x == self.ghost2.x and self.pacman.y == self.ghost2.y):
            return -1
        elif self.doesEatAllFoods():
            return 1
        else:
            return 0

    def ghostMove(self, gameMapArray, gh):
        direction = {0: "U", 1: "R", 2: "D", 3: "L"}
        while True:
            r = random.randint(0, 3)
            if r == 0 and self.mapGame.array[gh.x - 1][gh.y] != "#":
                return gh.x - 1, gh.y
            if r == 1 and self.mapGame.array[gh.x][gh.y + 1] != "#":
                return gh.x, gh.y + 1
            if r == 2 and self.mapGame.array[gh.x + 1][gh.y] != "#":
                return gh.x + 1, gh.y
            if r == 3 and self.mapGame.array[gh.x][gh.y - 1] != "#":
                return gh.x, gh.y - 1

    def validMove(self, x, y, move):
        if move == "U":
            x -= 1
        if move == "R":
            y += 1
        if move == "D":
            x += 1
        if move == "L":
            y -= 1

        if self.mapGame.array[x][y] != "#":
            return x, y
        else:
            return -1

    def bestMove(self, target):
        move = "D"
        bestScore = float('-inf')
        for i in ["U", "R", "D", "L"]:
            if self.validMove(self.pacman.x, self.pacman.y, i) != -1:
                pacman_future_x, pacman_future_y = self.validMove(self.pacman.x, self.pacman.y, i)
                pacman_now_x, pacman_now_y = self.pacman.x, self.pacman.y
                self.pacman.x, self.pacman.y = pacman_future_x, pacman_future_y

                food = self.mapGame.array[pacman_future_x][pacman_future_y]

                score = self.minimax(0, target, 0)

                self.pacman.x, self.pacman.y = pacman_now_x, pacman_now_y
                self.mapGame.array[pacman_future_x][pacman_future_y] = food

                if score > bestScore:
                    bestScore = score
                    move = i

        x, y = self.validMove(self.pacman.x, self.pacman.y, move)
        self.mapGame.array[x][y] = " "
        return self.validMove(self.pacman.x, self.pacman.y, move)

    def minimax(self, currentDepth, targetDepth, isMaximizing):
        if currentDepth == targetDepth:
            self.score = self.scoreFunction()
            return self.score

        if isMaximizing == 0:
            bestScore = float('-inf')
            for i in ["U", "R", "D", "L"]:
                if self.validMove(self.pacman.x, self.pacman.y, i) != -1:
                    pacman_future_x, pacman_future_y = self.validMove(self.pacman.x, self.pacman.y, i)
                    pacman_now_x, pacman_now_y = self.pacman.x, self.pacman.y

                    food = self.mapGame.array[pacman_future_x][pacman_future_y]

                    self.pacman.x, self.pacman.y = pacman_future_x, pacman_future_y

                    score = self.minimax(currentDepth, targetDepth, 1)

                    self.mapGame.array[pacman_future_x][pacman_future_y] = food
                    self.pacman.x, self.pacman.y = pacman_now_x, pacman_now_y

                    bestScore = max(bestScore, score)
            return bestScore
        elif isMaximizing == 1:
            bestScore = float('inf')
            for i in ["U", "R", "D", "L"]:
                if self.validMove(self.ghost1.x, self.ghost1.y, i) != -1:
                    ghost1_future_x, ghost1_future_y = self.validMove(self.ghost1.x, self.ghost1.y, i)
                    ghost1_now_x, ghost1_now_y = self.ghost1.x, self.ghost1.y

                    self.ghost1.x, self.ghost1.y = ghost1_future_x, ghost1_future_y

                    score = self.minimax(currentDepth, targetDepth, 2)

                    self.ghost1.x, self.ghost1.y = ghost1_now_x, ghost1_now_y

                    bestScore = min(bestScore, score)
            return bestScore
        elif isMaximizing == 2:
            bestScore = float('inf')
            for i in ["U", "R", "D", "L"]:
                if self.validMove(self.ghost2.x, self.ghost2.y, i) != -1:
                    ghost2_future_x, ghost2_future_y = self.validMove(self.ghost2.x, self.ghost2.y, i)
                    ghost2_now_x, ghost2_now_y = self.ghost2.x, self.ghost2.y

                    self.ghost2.x, self.ghost2.y = ghost2_future_x, ghost2_future_y

                    score = self.minimax(currentDepth + 1, targetDepth, 0)

                    self.ghost2.x, self.ghost2.y = ghost2_now_x, ghost2_now_y

                    bestScore = min(score, bestScore)
            return bestScore

    def scoreFunction(self):
        fromGhost1 = math.sqrt(
            (self.pacman.x - self.ghost1.x) ** 2 + (self.pacman.y - self.ghost1.y) ** 2)
        fromGhost2 = math.sqrt(
            (self.pacman.x - self.ghost2.x) ** 2 + (self.pacman.y - self.ghost2.y) ** 2)

        closest = float('inf')
        A = math.sqrt((self.mapGame.height - 2) ** 2 + (self.mapGame.width - 2) ** 2)
        for i in range(self.mapGame.height):
            for j in range(self.mapGame.width):
                if self.mapGame.array[i][j] == "+":
                    fromFood = math.sqrt(((self.pacman.x - i) ** 2) + (self.pacman.y - j) ** 2)
                    if fromFood < closest:
                        closest = fromFood

        self.score += ((A - closest) / A) * 9

        if min(fromGhost1, fromGhost2) < 3:
            self.score *= -1

        return self.score

    def startGame(self, target, turn):
        i = 0
        while True:
            i += 1
            self.printGame()
            if self.finishGame() == -1:
                print("GAME OVER")
                break
            elif self.finishGame() == 1:
                print("YOU WIN")
                break

            if turn == 0:
                self.pacman.x, self.pacman.y = self.bestMove(target)
                turn = 1
            if turn == 1:
                self.ghost1.x, self.ghost1.y = self.ghostMove(self.mapGame.array, self.ghost1)
                turn = 2
            if turn == 2:
                self.ghost2.x, self.ghost2.y = self.ghostMove(self.mapGame.array, self.ghost2)
                turn = 0
            # sleep(0.01)
            # os.system("cls")


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
                       else "+" for j in range(self.width)] for i in range(self.height)]

        self.array[1][1] = " "

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


game.startGame(1, 0)
