import pygame, sys, time, random, pygame_textinput
from pygame.locals import *

# Game Info
pygame.init()
screenWidth = 740
screenHeight = 580
screen = pygame.display.set_mode((screenWidth,screenHeight), 0, 32)
pygame.display.set_caption('Python')
clock = pygame.time.Clock()
screen.fill((0,0,0))


# DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
textinput = pygame_textinput.TextInput()

# Snake Globals
score = 0
headPos = [320, 240]
segments = [[320, 240]]
xvel = 0
yvel = 0
currentDirection = 0
snakeHead = 0
snakeHeadBox = 0

# Apple Globals
applePos = [0]
apples = 0
appleBox = pygame.Rect(1, 1, 20,20)
appleSpawn = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620] #length - 33

music = ('elevatorMusic.mp3', 'Fiberitron Loop.wav', 'kokomoMusic.mp3', 'marimbaMusic.mp3', 'pigstep.mp3')
# Draw Grid Function
def drawGrid(screen, color, pos):
    i = 0
    k = 0
    colorNo = 0
    while k<29:
        i=0
        pos[1] = pos[1] + 20
        pos[0] = -20
        k+=1
        while i<37:
            if colorNo % 2 == 0:
                color = (47, 161, 45)
            else:
                color = (61, 214, 58)
            pos = [pos[0]+20, pos[1]]
            pygame.draw.rect(screen, color, (pos[0],pos[1],20,20))
            i+=1
            colorNo +=1

drawGrid(screen, (255,255,255), [-20,-20])


# Text Frame
def text(msg, color, x, y, size):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, color)
    screen.blit(text, (x, y))


# Leaderboard Scores
leaderboard = []
highscoreFile = open('highscoreFile.txt', 'r')
nameFile = open('nameFile.txt', 'r')

for i in range(3):

    highscoreStr = list(highscoreFile.readline().rstrip("\n"))
    difficulty = highscoreStr[-1]
    highscoreStr.pop()

    highscoreInt=''
    for i in highscoreStr:
        highscoreInt+= i
        
    leaderboard.append( [int(highscoreInt), nameFile.readline().rstrip("\n"), difficulty] )
    print(leaderboard)

highscoreFile.close()
nameFile.close()


def printLeaderboard():
    text("Leaderboard", (173, 12, 0), 230, 350, 70)
    textY = 430
    for i in leaderboard:
        if i[1] != '':
            nameText = i[1]

        else:
            nameText = '___'
        if i[2] == 'e':
            color = (121, 255, 71)
        elif i[2] == 'm':
            color = (245, 192, 0)
        elif i[2] == 'h':
            color = (255,0,0)
        else:
            color = (0,0,0)
        text(nameText, color, 220, textY, 50)
        text(str(i[0]), (0,0,0), 525, textY, 50)
        textY+=50

def playAgain():
    global score, headPos, segments, xvel, yvel, currentDirection, snakeHead, snakeHeadBox, applePos, apples, increase, tick, difficulty, gameOver
    gameOver = False
    score = 0
    headPos = [320, 240]
    segments = [[320, 240]]
    xvel = 0
    yvel = 0
    currentDirection = 0
    snakeHead = 0
    snakeHeadBox = pygame.Rect(headPos[0],headPos[1],20,20)
    applePos = (appleSpawn[random.randint(0, 30)], appleSpawn[random.randint(0, 23)])
    apples = 0
    
    

# Button Class
class button:
    def __init__(self, pos, width, height, color, mouseOverColor, originalColor, text, textSize):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.mouseOverColor = mouseOverColor
        self.originalColor = originalColor
        self.text = text
        self.textSize = textSize

    def draw(self):
        font = pygame.font.SysFont('freesansbold.ttf', self.textSize)
        pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], self.width, self.height]) 

        if self.color == (128,0,128):
            textColor = (0,0,255)
        else:
            textColor = (128,0,128)

        text(self.text, textColor, self.pos[0]+(self.width-font.size(self.text)[0])/2, self.pos[1]+15, self.textSize)

    def check(self, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pos[0] >= self.pos[0] and pos[0] <= self.pos[0] + self.width and pos[1] >= self.pos[1] and pos[1] <= self.pos[1] + self.height:                    
                return True

            else:
                return False

        if event.type == pygame.MOUSEMOTION: 
            if pos[0] >= self.pos[0] and pos[0] <= self.pos[0] + self.width and pos[1] >= self.pos[1] and pos[1] <= self.pos[1] + self.height:
                self.color = self.mouseOverColor
                
            else:
                self.color = self.originalColor

startGameButton = button((240, 160), 280, 80, (0,0,255), (128,0,128), (0,0,255), "Start Game", 70)
playAgainButton = button((150, 160), 200, 60, (0, 0, 255), (128,0,128), (0,0,255), "Play Again", 50)
quitButton = button((410, 160), 200, 60, (0, 0, 255), (128,0,128), (0,0,255), "Quit", 50)
easyButton = button((35, 260), 200, 60, (0, 0, 255), (128,0,128), (0,0,255), "Easy", 50)
mediumButton = button((270, 260), 200, 60, (0, 0, 255), (128,0,128), (0,0,255), "Medium", 50)
hardButton = button((505, 260), 200, 60, (0, 0, 255), (128,0,128), (0,0,255), "Hard", 50)
changeMusicButton = button((250,260), 260, 60, (128,0,128), (0,0,255), (128,0,128), "Change Music", 50)


class segment:
    def __init__(self, pos):
        self.pos = pos


class snake:
    def __init__(self, color):
        self.name = color
        self.color = color

    def restart(self, snakeLength):
        global headPos
        global snakeHead
        global snakeHeadBox
        global score

        snakeHeadBox = pygame.Rect(headPos[0],headPos[1],20,20)
        snakeHead = pygame.draw.rect(screen, self.color, (headPos[0], headPos[1],20,20))
        
        pygame.draw.rect(screen, (255,255,255), (headPos[0], headPos[1],20,20))
        pygame.draw.rect(screen, (0,0,0), (headPos[0], headPos[1],17,17))
        
        for i in segments [1:]:
            pygame.draw.rect(screen, (255,255,255), (i.pos[0], i.pos[1],20,20))
            pygame.draw.rect(screen, (0,0,0), (i.pos[0], i.pos[1],17,17))
        
        # Score
        text("Score: "+str(score), (255, 255, 255), 10, 550, 30)


    def grow(self):
        global headPos
        global segments
        global score

        score += 1
        
        if currentDirection == 1:
            add1 = 0
            add2 = 20

        elif currentDirection == 2:
            add1 = 20
            add2 = 0
        
        elif currentDirection == 3:
            add1 = 0
            add2 = -20
        
        elif currentDirection == 4:
            add1 = -20
            add2 = 0

        if len(segments) > 1:
            newPart = segment([segments[-1].pos[0]+add1, segments[-1].pos[1]+add2])
        
        else:
            newPart = segment([segments[-1][0]+add1, segments[-1][1]+add2])

        segments.append(newPart)
        
    
    def direction(self, directionIn):
        global currentDirection
        # Direction  |  1 = up  |  2 = left  |  3 = down  |  4 = right  |
        
        if directionIn < 3 and directionIn + 2 == currentDirection:
            return
        elif directionIn == 3 and currentDirection == 1:
            return
        elif directionIn == 4 and currentDirection == 2:
            return
        currentDirection = directionIn

        
    def movement(self):
        global xvel 
        global yvel
        global currentDirection
        
        xvel = 0
        yvel = 0
        if currentDirection == 1:
            yvel = -20
        elif currentDirection == 2:
            xvel = -20
        elif currentDirection == 3:
            yvel = 20
        elif currentDirection == 4:
            xvel = 20
        

class apple:
    def __init__(self):
        global applePos

        applePos = (appleSpawn[random.randint(0, 30)], appleSpawn[random.randint(0, 23)])
        pygame.draw.rect(screen, (255,0,0), (applePos[0], applePos[1], 20,20))
        
    
    def redraw(self):
        global applePos
        global apples
        global appleBox

        appleBox = pygame.Rect(applePos[0], applePos[1], 20,20)
        apples = pygame.draw.rect(screen, (255,0,0), (applePos[0], applePos[1], 20,20))
    
tick = 10


pygame.mixer.music.load('elevator Music.mp3')
pygame.mixer.music.play(-1)
oldScore = 0

run = True
# Start Game Button
text("SNAKE", (255, 0, 0), 180, 20, 158)
clicked = False
song=0
while not clicked:

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        startGameButton.draw()
        if startGameButton.check(pos):
            
            clicked = True
        
        changeMusicButton.draw()
        if changeMusicButton.check(pos):

            song+=1
            if song > 4:
                song = 0
            pygame.mixer.music.load(music[song])
            pygame.mixer.music.play(-1)
        

        printLeaderboard()
    pygame.display.update()

# Title
drawGrid(screen, (255,255,255), [-20,-20])
p1 = snake((250, 10, 230))
p1.restart(1)
food = apple()
# Choose Mode
gameOver = False
while clicked:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        easyButton.draw()
        if easyButton.check(pos):
            tick = 8
            increase = 2
            difficulty = 'e'
            clicked = False
        
        mediumButton.draw()
        if mediumButton.check(pos):
            tick = 10
            increase = 4
            difficulty = 'm'
            clicked = False
        
        hardButton.draw()
        if hardButton.check(pos):
            tick = 15
            increase = 6
            difficulty = 'h'
            clicked = False

        pygame.display.update()

while run:
    clock.tick(tick)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    

    if keys[pygame.K_UP]:
        p1.direction(1)
        p1.movement()


    elif keys[pygame.K_LEFT]:
        p1.direction(2)
        p1.movement()


    elif keys[pygame.K_DOWN]:
        p1.direction(3)
        p1.movement()


    elif keys[pygame.K_RIGHT]:
        p1.direction(4)
        p1.movement()

    oldx = headPos[0]
    oldy = headPos[1]

    
    headPos[0] = headPos[0] + xvel
    headPos[1] = headPos[1] + yvel
    segments[0][0] = headPos[0]
    segments[0][1] = headPos[1]

    # Move Snake
    for x in segments[1:]:
        jj = x.pos[0]
        x.pos[0] = oldx
        oldx = jj

    for y in segments[1:]:
        jj = y.pos[1]
        y.pos[1] = oldy
        oldy = jj
    
    # Check if Snake Eats Apple
    if snakeHeadBox.colliderect(appleBox):
        p1.grow()
        del food
        food = apple() 

    if score % 5 == 0 and score != 0:
        if score != oldScore:
            tick += increase
            print(tick)
        oldScore = score 


    # Check it hasn't run into itself
    for i in segments[1:]:
        for j in segments[1:]:
            if i != j and i.pos == j.pos:
                gameOver = True

    # Game over code (and check if hit wall)
    if headPos[0] < 0 or headPos[0] > 720 or headPos[1] < 0 or headPos[1] > 560 or gameOver:
        text("GAME OVER", (255, 0, 0), 160, 50, 100)
        text("Created by ", (255,255,255), 145, 5, 50)
        text("Vidster Studios", (255,0,0), 338, 5, 50)
        pygame.display.update() 

        # Check If New Highscore
        if score > leaderboard[2][0]:
            
            if score > leaderboard[0][0]:
                text("NEW HIGHSCORE!", (90,90,0), 235, 120, 50)
            else:
                text("TOP 3 SCORE!", (90,90,0), 270, 120, 50)

            text("What's your name?", (255,0,0), 210, 250, 50)

            # Text Input
            typing = True
            while typing:
                events = pygame.event.get()
                for event in events:
                    pos = pygame.mouse.get_pos()
                    
                    if event.type == pygame.QUIT or quitButton.check(pos):
                        quit()
                    
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_RETURN]:
                        name = textinput.get_text().strip()
                        typing = False
                            
                quitButton.draw()

                pygame.draw.rect(screen, (255,255,255), (20,300,700,40))
                screen.blit(textinput.get_surface(), (30,306))
                textinput.update(events)
                
                pygame.display.update()

            textinput.clear_text()

            # Update Leaderboard
            leaderboard[2][1] = name
            leaderboard[2][0] = score
            leaderboard[2][2] = difficulty
            leaderboard.sort(reverse=True)
            
            highscoreFile = open('highscoreFile.txt', 'w')
            nameFile = open('nameFile.txt', 'w')

            for i in leaderboard:
                highscoreFile.write(str(i[0])+i[2]+'\n')
                nameFile.write(i[1]+"\n")

            highscoreFile.close()
            nameFile.close() 
    
        # Leaderboard
        printLeaderboard()
        pygame.display.update() 
        clicked = True
        pos = (0,0)
        while clicked:
            
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

            quitButton.draw()
            if event.type == pygame.QUIT or quitButton.check(pos):
                quit()
            
            playAgainButton.draw()
            if playAgainButton.check(pos):
                clicked = True
                while clicked:
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()

                        if event.type == pygame.QUIT:
                            run = False
                            pygame.quit()
                            quit()

                        easyButton.draw()
                        if easyButton.check(pos):
                            tick = 8
                            increase = 2
                            difficulty = 'e'
                            clicked = False
                        
                        mediumButton.draw()
                        if mediumButton.check(pos):
                            tick = 10
                            increase = 4
                            difficulty = 'm'
                            clicked = False
                        
                        hardButton.draw()
                        if hardButton.check(pos):
                            tick = 15
                            increase = 6
                            difficulty = 'h'
                            clicked = False

                        pygame.display.update()
                        playAgain()
                            

            pygame.display.update()



    drawGrid(screen, (255,255,255), [-20,-20])
    p1.restart(1)
    food.redraw()
    pygame.display.update()