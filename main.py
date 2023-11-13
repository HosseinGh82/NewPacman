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


class Ghost:
    def __init__(self, locX, locY):
        self.x = locX
        self.y = locY


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
        self.array[4][3] = "#"
        self.array[4][16] = "#"
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
